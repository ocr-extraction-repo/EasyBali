from app.db.session import order_collection, db, villa_code_collection
from pymongo import ReturnDocument
from datetime import datetime
from app.models.order_summary import Order
from typing import Dict, Optional


active_chat_sessions: Dict[str, Order] = {}
order_sessions: Dict[str, str] = {}


async def get_user_villa_code(sender_id: str):
    try:
        document = await villa_code_collection.find_one({"sender_id": sender_id})    
        if document:
            return document.get("villa_code")
        else:
            return None
    except Exception as e:
        print(f"Error retrieving villa code: {e}")
        return None


async def get_next_order_id() -> str:
    counter_doc = await db.counters.find_one_and_update(
        {"_id": "order_number"},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return f"EB{counter_doc['sequence_value']:0d}"


async def initiate_chat_session(sender_id: str, service_name: str, person_count: str, base_price: str, date: datetime = None, time: str = None) -> Order:
    order_number = await get_next_order_id()
    
    user_villa_code = await get_user_villa_code(sender_id)
   
    try:
        persons = int(person_count)
        unit_price = int(base_price.replace(",", "").replace(" ", ""))
        total_price = unit_price * persons
        formatted_price = f"{total_price:,}"
    except (ValueError, AttributeError):
        formatted_price = base_price

    new_order = Order(
        order_number=order_number,
        service_name=service_name,
        sender_id=sender_id,
        date=date,
        time=time,
        price=formatted_price,
        confirmation=False,
        villa_code=user_villa_code,
        status="pending",
    )
    order_sessions[sender_id] = new_order.order_number
    return new_order


async def save_order_to_db(order: dict):
    await order_collection.insert_one(order)


def format_order_summary(order: dict) -> str:
    order_date = order.get("date")
    if order_date and isinstance(order_date, datetime):
        order_date = order_date.strftime("%Y-%m-%d")
    elif isinstance(order_date, str):
        order_date = order_date
    else:
        order_date = "N/A"
    
    summary_lines = [
        f"Order ID: {order.get('order_number', 'N/A')}",
        f"Service: {order.get('service_name', 'N/A')}",
        f"Date: {order_date}",
        f"Time: {order.get('time', 'N/A')}",
        f"Price: {order.get('price', 'N/A')}",
    ]
    return "\n".join(summary_lines)



async def check_order_confirmation(order_number: str) -> bool:
    order_doc: Optional[dict] = await order_collection.find_one({"order_number": order_number})
    if order_doc is not None:
        return order_doc.get("confirmation")
    else:
        return {f"No order found"}
    

async def update_order_confirmation(order_number: str, confirmation: bool) -> str:
    updated_order = await order_collection.find_one_and_update(
        {"order_number": order_number},
        {"$set": {"confirmation": confirmation}},
        return_document=ReturnDocument.AFTER
    )
    if updated_order:
        return updated_order.get("sender_id")
    return None


async def get_sender_id_by_order(order_number: str) -> Optional[str]:
    order = await order_collection.find_one({"order_number": order_number})
    if order:
        return order.get("sender_id")
    return None


async def get_order_by_number(order_number: str) -> Optional[dict]:
    try:
        order_doc = await order_collection.find_one({"order_number": order_number})
        
        if not order_doc:
            return None
        return {
            "order_number": order_doc.get("order_number"),
            "service_name": order_doc.get("service_name"),
            "date": order_doc.get("date").strftime("%d-%m-%Y") if order_doc.get("date") else "N/A",
            "time": order_doc.get("time"),
            "price": order_doc.get("price"),
            "sender_id": order_doc.get("sender_id"),
            "status": order_doc.get("status")
        }
        
    except Exception as e:
        print(f"Error fetching order {order_number}: {e}")
        return None
    
