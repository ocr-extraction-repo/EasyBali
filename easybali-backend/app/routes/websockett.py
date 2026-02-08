from app.services.websocket_managerr import ConnectionManager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, BackgroundTasks
from app.db.session import order_collection
from app.models.order_summary import WebOrder
from app.services.order_summary import get_next_order_id
import uuid
from app.utils.whatsapp_func import fetch_whatsapp_numbers, send_whatsapp_order_to_SP

manager = ConnectionManager()
router = APIRouter(tags=["Sessions"])


@router.post("/create-session")
async def create_session(order_data: WebOrder, background_tasks: BackgroundTasks):
    session_id = str(uuid.uuid4())
    ordernumber = await get_next_order_id()
    
    # Clean and convert price (remove spaces and convert to float)
    original_price = float("".join(order_data.price.split()))
    no_of_person = int(order_data.no_of_person)
    final_price = no_of_person * original_price
    
    order = {
        "sender_id": session_id,
        "order_number": ordernumber,
        "service_name": order_data.service_name,
        "date": order_data.date,
        "time": order_data.time,
        "price": order_data.price, 
        "original_price": original_price,
        "final_price": final_price, 
        "no_of_person": order_data.no_of_person,
        "phone_number": order_data.phone_number,
        "name": order_data.name,
        "confirmation": False,
        "session_active": True,
        "payment_status": "pending"
    }

    await order_collection.insert_one(order)
    whatsapp_numbers = await fetch_whatsapp_numbers(order_data.service_name)

    for number in whatsapp_numbers:
        background_tasks.add_task(send_whatsapp_order_to_SP, number, order)
    
    return {
        "message": "Thank you for your booking. Please wait for confirmation.",
        "session_id": session_id,
    }

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