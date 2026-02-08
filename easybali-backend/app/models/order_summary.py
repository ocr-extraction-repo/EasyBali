import datetime
from typing import Optional
from pydantic import BaseModel

class PaymentInfo(BaseModel):
    xendit_invoice_id: Optional[str] = None
    payment_url: Optional[str] = None
    external_id: Optional[str] = None
    payment_status: str = "unpaid"
    payment_method: Optional[str] = None
    paid_at: Optional[datetime.datetime] = None

class Order(BaseModel):
    sender_id: str
    order_number: str
    service_name: str
    date: Optional[datetime.datetime] = None
    time: Optional[str] = None
    price: Optional[str] = None
    confirmation: bool = False
    status: str = "pending"
    payment: PaymentInfo = PaymentInfo()
    service_provider_code:Optional[str] = None
    villa_code:str = None
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()

class WebOrder(BaseModel):
    service_name: str
    name:str
    date: Optional[datetime.datetime] = None
    time: Optional[str] = None
    price: Optional[str] = None
    no_of_person:Optional[str]=None
    phone_number:Optional[str]=None
    confirmation: bool = False
    payment: PaymentInfo = PaymentInfo()