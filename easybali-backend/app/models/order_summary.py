import datetime
from typing import Optional
from pydantic import BaseModel, Field

class PaymentInfo(BaseModel):
    xendit_invoice_id: Optional[str] = None
    payment_url: Optional[str] = None
    external_id: Optional[str] = None
    payment_status: str = "unpaid"
    payment_method: Optional[str] = None
    paid_at: Optional[datetime.datetime] = None
    
    # Error recovery fields
    retry_count: int = 0
    retry_history: list = Field(default_factory=list)
    regeneration_history: list = Field(default_factory=list)
    failure_reason: Optional[str] = None
    distribution_error: Optional[str] = None

class Order(BaseModel):
    sender_id: str
    order_number: str
    service_name: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    date: Optional[datetime.datetime] = None
    time: Optional[str] = None
    price: Optional[str] = None
    confirmation: bool = False
    status: str = "pending"
    payment: PaymentInfo = Field(default_factory=PaymentInfo)
    service_provider_code:Optional[str] = None
    villa_code: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class WebOrder(BaseModel):
    service_name: str
    name: str
    phone_number: Optional[str] = None
    villa_code: Optional[str] = None
    date: Optional[datetime.datetime] = None
    time: Optional[str] = None
    price: Optional[str] = None
    no_of_person:Optional[str]=None
    confirmation: bool = False
    payment: PaymentInfo = Field(default_factory=PaymentInfo)
