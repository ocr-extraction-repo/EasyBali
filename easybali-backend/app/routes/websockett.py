from app.services.websocket_managerr import ConnectionManager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, BackgroundTasks, HTTPException, Request
from app.db.session import order_collection
from app.models.order_summary import WebOrder, Order
from app.services.order_summary import get_next_order_id
import uuid
import re
import datetime
from app.utils.whatsapp_func import fetch_whatsapp_numbers, send_whatsapp_order_to_SP
from app.settings.config import settings
from app.services.payment_service import create_xendit_payment_with_distribution, update_order_with_payment_info
import logging

manager = ConnectionManager()
router = APIRouter(tags=["Sessions"])
logger = logging.getLogger(__name__)


def _assert_non_production_testing():
    if settings.APP_ENV.lower() == "production":
        raise HTTPException(status_code=403, detail="Testing endpoints are disabled in production")

def _assert_testing_token(request: Request):
    # Basic guard so this can't be triggered accidentally on a public staging URL.
    token = request.headers.get("x-testing-token")
    if not token or token != settings.XENDIT_WEBHOOK_CALLBACK_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized testing token")


@router.post("/create-session")
async def create_session(order_data: WebOrder, background_tasks: BackgroundTasks):
    try:
        session_id = str(uuid.uuid4())
        ordernumber = await get_next_order_id()
        
        # Clean and convert price
        cleaned_price = re.sub(r"[^\d]", "", str(order_data.price or "0"))
        original_price = float(cleaned_price or "0")
        if not order_data.no_of_person:
            raise ValueError("no_of_person is required")
        no_of_person = int(order_data.no_of_person)
        final_price = no_of_person * original_price
        
        order = {
            "sender_id": session_id,
            "order_number": ordernumber,
            "service_name": order_data.service_name,
            "name": order_data.name,
            "phone_number": order_data.phone_number,
            "villa_code": order_data.villa_code,
            "date": order_data.date,
            "time": order_data.time,
            "price": str(int(final_price)),
            "original_price": original_price,
            "final_price": final_price, 
            "no_of_person": order_data.no_of_person,
            "confirmation": False,
            "session_active": True,
            "payment_status": "pending"
        }

        await order_collection.insert_one(order)

        # Provider notifications should never block session creation.
        try:
            whatsapp_numbers = await fetch_whatsapp_numbers(order_data.service_name)
            for number in whatsapp_numbers or []:
                background_tasks.add_task(send_whatsapp_order_to_SP, number, order)
        except Exception as notify_err:
            logger.warning(f"Provider notify skipped for order {ordernumber}: {notify_err}")
        
        return {
            "message": "Thank you for your booking. Please wait for confirmation.",
            "session_id": session_id,
            "order_number": ordernumber,
        }
    except Exception as e:
        logger.exception(f"create-session failed: {e}")
        # Surface details in staging/dev to unblock testing.
        if settings.APP_ENV.lower() != "production":
            raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/testing/session/{session_id}")
async def get_testing_session_state(session_id: str):
    _assert_non_production_testing()
    session = await order_collection.find_one({"sender_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    payment_doc = session.get("payment", {})
    return {
        "session_id": session_id,
        "order_number": session.get("order_number"),
        "service_name": session.get("service_name"),
        "status": session.get("status"),
        "payment_status": payment_doc.get("payment_status") or session.get("payment_status"),
        "payment_url": payment_doc.get("payment_url"),
        "xendit_invoice_id": payment_doc.get("xendit_invoice_id"),
        "external_id": payment_doc.get("external_id")
    }


@router.get("/testing/order/{order_number}")
async def get_testing_order_state(order_number: str):
    _assert_non_production_testing()
    session = await order_collection.find_one({"order_number": order_number})
    if not session:
        raise HTTPException(status_code=404, detail="Order not found")

    payment_doc = session.get("payment", {})
    return {
        "session_id": session.get("sender_id"),
        "order_number": order_number,
        "service_name": session.get("service_name"),
        "status": session.get("status"),
        "payment_status": payment_doc.get("payment_status") or session.get("payment_status"),
        "payment_url": payment_doc.get("payment_url"),
        "xendit_invoice_id": payment_doc.get("xendit_invoice_id"),
        "external_id": payment_doc.get("external_id")
    }


@router.post("/testing/auto-confirm/{session_id}")
async def auto_confirm_and_create_payment_link(session_id: str, request: Request):
    """
    Staging-only helper:
    - Marks a website booking as confirmed (simulates provider accept)
    - Generates a Xendit invoice/payment link immediately
    - Pushes the link into the WebSocket session (or queues it until WS connects)
    """
    _assert_non_production_testing()
    _assert_testing_token(request)

    session = await order_collection.find_one({"sender_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    order_number = session.get("order_number")
    if not order_number:
        raise HTTPException(status_code=400, detail="Session missing order_number")

    # Mark as confirmed so downstream logic sees it as accepted.
    await order_collection.update_one(
        {"sender_id": session_id},
        {"$set": {
            "confirmation": True,
            "confirmed_by_provider": "testing",
            "confirmed_at": datetime.datetime.now(),
            "status": "confirmed_testing"
        }}
    )

    # Re-read to pick up changes
    session = await order_collection.find_one({"sender_id": session_id})

    order = Order(
        sender_id=session_id,
        order_number=order_number,
        service_name=session.get("service_name"),
        date=session.get("date"),
        time=session.get("time"),
        price=str(session.get("price") or session.get("final_price") or "0"),
        confirmation=True,
        status=session.get("status") or "pending",
        service_provider_code=session.get("service_provider_code"),
        villa_code=session.get("villa_code"),
        name=session.get("name"),
        phone_number=session.get("phone_number"),
    )

    payment_result = await create_xendit_payment_with_distribution(order)
    if not payment_result.get("success"):
        raise HTTPException(status_code=500, detail=payment_result.get("error") or "Payment link creation failed")

    await update_order_with_payment_info(order_number, payment_result)

    payment_url = payment_result.get("payment_url")
    if payment_url:
        msg = f"Payment link for order {order_number}: [link]({payment_url})"
        await manager.send_personal_message(
            message=msg,
            session_id=session_id,
            message_type="link_message"
        )

    return {
        "success": True,
        "session_id": session_id,
        "order_number": order_number,
        "payment_url": payment_url,
        "distribution_warning": payment_result.get("distribution_warning"),
    }


@router.get("/testing/diag")
async def testing_diagnostics(request: Request):
    _assert_non_production_testing()
    _assert_testing_token(request)

    import os
    raw_uri = settings.MONGO_URI or os.environ.get("MONGO_URI", "")
    # Show only the cluster hostname (not credentials) for security
    try:
        cluster_hint = raw_uri.split("@")[-1].split("/")[0] if "@" in raw_uri else "unknown"
    except Exception:
        cluster_hint = "parse-error"

    diag = {"mongo_ping": None, "next_order_id": None, "mongo_cluster": cluster_hint}
    try:
        # Ping Mongo via the underlying database.
        await order_collection.database.command("ping")
        diag["mongo_ping"] = "ok"
    except Exception as e:
        diag["mongo_ping"] = f"error: {e}"

    try:
        diag["next_order_id"] = await get_next_order_id()
    except Exception as e:
        diag["next_order_id"] = f"error: {e}"

    return diag

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    session = await order_collection.find_one(
        {"sender_id": session_id, "session_active": True}
    )
    
    if not session:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        await manager.connect(session_id, websocket)
        try:
            while True:
                await websocket.receive_text()
                    
        except WebSocketDisconnect:
            print(f"WebSocket disconnected for {session_id}")
            manager.disconnect(session_id)
        except Exception as e:
            print(f"Error in WebSocket connection for {session_id}: {e}")
            manager.disconnect(session_id)
            
    except Exception as e:
        print(f"Failed to establish WebSocket connection for {session_id}: {e}")
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except:
            pass
