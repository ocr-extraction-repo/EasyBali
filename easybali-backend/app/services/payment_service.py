import re
import httpx
import xendit
import base64
from xendit.apis import InvoiceApi
from xendit.invoice.model.invoice import Invoice
from xendit.invoice.model.create_invoice_request import CreateInvoiceRequest
from xendit.invoice.model.customer_object import CustomerObject
from xendit.invoice.model.notification_preference import NotificationPreference
from xendit.invoice.model.notification_channel import NotificationChannel
from xendit.invoice.model.invoice_item import InvoiceItem
import datetime
from app.db.session import order_collection
from app.models.order_summary import Order
from app.settings.config import settings
import logging


logger = logging.getLogger(__name__)

# Set API key
xendit.set_api_key(settings.XENDIT_SECRET_KEY)


def clean_price_string(price_str: str) -> int:
    cleaned = re.sub(r'[^\d]', '', price_str)
    
    if not cleaned:
        raise ValueError(f"No digits found in price string: '{price_str}'")
    
    return int(cleaned)


async def get_service_provider_bank_details(provider_code: str) -> dict:
    """Fetch service provider bank details from API"""
    try:
        params = {"provider_code": provider_code}
        url = "https://easy-bali.onrender.com/menu/service-provider-bank"
        
        print(f"🔍 Fetching provider bank details for: '{provider_code}'")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            print(f"🔍 Request URL: {response.url}")
            print(f"🔍 Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"🔍 Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        print(f"Error fetching service provider bank details: {e}")
        return None


async def get_villa_bank_details(provider_code: str) -> dict:
    """Fetch villa bank details from API"""
    try:
        params = {"provider_code": provider_code}
        url = "https://easy-bali.onrender.com/menu/villa-bank"
        
        print(f"🔍 Fetching villa bank details for: '{provider_code}'")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            print(f"🔍 Request URL: {response.url}")
            print(f"🔍 Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"🔍 Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        print(f"Error fetching villa bank details: {e}")
        return None


async def get_price_distribution(service_item: str) -> dict:
    """Fetch price distribution for service item"""
    try:
        params = {"service_item": service_item}
        url = "https://easy-bali.onrender.com/menu/price_distribution"
        
        print(f"🔍 Fetching price distribution for: '{service_item}'")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            print(f"🔍 Request URL: {response.url}")
            print(f"🔍 Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"🔍 Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        print(f"Error fetching price distribution: {e}")
        return None

# Enhanced payment creation function
async def create_xendit_payment_with_distribution(order: Order):
    """Create payment invoice and prepare distribution data"""
    try:
        # Get price distribution
        price_distribution = await get_price_distribution(order.service_name)
        if not price_distribution:
            return {
                'success': False,
                'error': 'Unable to fetch price distribution'
            }
        
        # Get bank details for both parties
        service_provider_bank = await get_service_provider_bank_details(order.service_provider_code)
        villa_bank = await get_villa_bank_details(order.villa_code)
        
        if not service_provider_bank or not villa_bank:
            return {
                'success': False,
                'error': 'Unable to fetch bank details'
            }
        
        external_id = f"booking_{order.order_number}_{int(datetime.datetime.now().timestamp())}"
        
        try:
            price_clean = clean_price_string(order.price)
            service_provider_price = clean_price_string(price_distribution['service_provider_price'])
            villa_price = clean_price_string(price_distribution['villa_price'])
        except ValueError as e:
            print(f"Price cleaning error: {e}")
            return {
                'success': False,
                'error': f"Invalid price format: {order.price}"
            }
        
        # Create API client and instance
        api_client = xendit.ApiClient()
        api_instance = InvoiceApi(api_client)
        
        # Create invoice request
        create_invoice_request = CreateInvoiceRequest(
            external_id=external_id,
            amount=float(price_clean),
            currency='IDR',
            invoice_duration=86400.0,  # 24 hours in seconds
            description=f"Payment for {order.service_name} on {order.date.strftime('%d-%m-%Y')} at {order.time}",
            customer=CustomerObject(
                given_names='Customer',
                mobile_number=order.sender_id,
            ),
            customer_notification_preference=NotificationPreference(
                invoice_created=[NotificationChannel("whatsapp")],
                invoice_reminder=[NotificationChannel("whatsapp")],
                invoice_paid=[NotificationChannel("whatsapp")]
            ),
            success_redirect_url=f"{settings.BASE_URL}/chatbot",
            failure_redirect_url=f"{settings.BASE_URL}/payment-failed?order={order.order_number}",
            webhook_url=f"{settings.BASE_URL}/webhook/xendit-payment",
            payment_methods = ["CREDIT_CARD", "BCA", "BNI", "BSI", "BRI", "MANDIRI", "PERMATA", "SAHABAT_SAMPOERNA", "BNC", "ALFAMART", "INDOMARET", "OVO", "DANA", "SHOPEEPAY", "LINKAJA", "JENIUSPAY", "DD_BRI", "DD_BCA_KLIKPAY", "QRIS"],
            items=[
                InvoiceItem(
                    name=order.service_name,
                    quantity=1.0,
                    price=float(price_clean),
                )
            ]
        )
        
        # Create the invoice
        api_response = api_instance.create_invoice(create_invoice_request)
        
        # Prepare distribution data
        distribution_data = {
            'service_provider': {
                'amount': service_provider_price,
                'bank_details': service_provider_bank
            },
            'villa': {
                'amount': villa_price,
                'bank_details': villa_bank
            },
            'total_distribution': service_provider_price + villa_price
        }
        
        return {
            'success': True,
            'invoice_id': api_response.id,
            'payment_url': api_response.invoice_url,
            'external_id': external_id,
            'expires_at': api_response.expiry_date,
            'distribution_data': distribution_data
        }
        
    except xendit.XenditSdkException as e:
        print(f"Xendit SDK Error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        print(f"Xendit Invoice Creation Error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Updated order update function
async def update_order_with_payment_info(order_number: str, payment_data: dict):
    """Update order with payment and distribution information"""
    try:
        update_data = {
            'payment.xendit_invoice_id': payment_data.get('invoice_id'),
            'payment.payment_url': payment_data.get('payment_url'),
            'payment.external_id': payment_data.get('external_id'),
            'payment.payment_status': 'pending',
            'payment.distribution_data': payment_data.get('distribution_data'),
            'status': 'payment_pending',
            'updated_at': datetime.datetime.now()
        }
        
        result = await order_collection.update_one(
            {"order_number": order_number},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Database update error: {str(e)}")
        return False
    

async def create_bank_disbursement(client: httpx.AsyncClient, amount: int, bank_details: dict, reference_id: str, description: str):
    try:
        # Build payload
        disbursement_data = {
            "external_id": reference_id,
            "amount": amount,  # must be int, no decimals
            "bank_code": str (bank_details.get("bank_code")),
            "account_holder_name": str (bank_details.get("account_name")),
            "account_number": bank_details.get("account_number"),
            "description": description
        }
        bank_code = disbursement_data["bank_code"]
        print(type(bank_code))

        # Proper Basic Auth header
        token = base64.b64encode(f"{settings.XENDIT_SECRET_KEY}:".encode()).decode()

        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            # "X-IDEMPOTENCY-KEY": reference_id  # Optional but recommended
        }

        # Send request
        response = await client.post(
            "https://api.xendit.co/disbursements",
            json=disbursement_data,
            headers=headers
        )
        response.raise_for_status()
        result = response.json()

        return {
            "success": True,
            "disbursement_id": result.get("id"),
            "status": result.get("status"),
            "amount": result.get("amount")
        }

    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e.response.text}")
        return {"success": False, "error": e.response.text}
    except Exception as e:
        print(f"Disbursement creation error: {str(e)}")
        return {"success": False, "error": str(e)}
    

async def distribute_order_payments(order_number: str, distribution_data: dict):
    try:
        async with httpx.AsyncClient() as client:
            sp_result = await create_bank_disbursement(
                client=client,
                amount=distribution_data['service_provider']['amount'],
                bank_details=distribution_data['service_provider']['bank_details'],
                reference_id=f"sp_{order_number}",
                description=f"Service provider payment for order {order_number}"
            )
            villa_result = await create_bank_disbursement(
                client=client,
                amount=distribution_data['villa']['amount'],
                bank_details=distribution_data['villa']['bank_details'],
                reference_id=f"villa_{order_number}",
                description=f"Villa commission for order {order_number}"
            )
            await order_collection.update_one(
                {"order_number": order_number},
                {
                    "$set": {
                        "payment.disbursements": {
                            "service_provider": sp_result,
                            "villa": villa_result,
                            "distributed_at": datetime.datetime.now()
                        },
                        "status": "funds_distributed"
                    }
                }
            )
            
            logger.info(f"Payments distributed successfully for order {order_number}")
            
    except Exception as e:
        logger.info(f"Distribution error for order {order_number}: {str(e)}")
        await order_collection.update_one(
            {"order_number": order_number},
            {
                "$set": {
                    "payment.distribution_error": str(e),
                    "status": "distribution_failed"
                }
            }
        )