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
import asyncio


logger = logging.getLogger(__name__)


def _set_xendit_api_key() -> bool:
    if not settings.XENDIT_SECRET_KEY:
        logger.error("XENDIT_SECRET_KEY is not configured")
        return False
    xendit.set_api_key(settings.XENDIT_SECRET_KEY)
    return True


def _resolve_xendit_webhook_url() -> str:
    path = settings.XENDIT_WEBHOOK_PATH or "/webhook/xendit"
    if not path.startswith("/"):
        path = f"/{path}"
    # Callbacks must target backend URL.
    callback_base = settings.BASE_URL or settings.WEB_BASE_URL
    return f"{callback_base}{path}"


def _should_distribute_payments() -> bool:
    return bool(settings.XENDIT_ENABLE_DISBURSEMENT)


def clean_price_string(price_str: str) -> int:
    cleaned = re.sub(r'[^\d]', '', price_str)
    
    if not cleaned:
        raise ValueError(f"No digits found in price string: '{price_str}'")
    
    return int(cleaned)


async def get_service_provider_bank_details(provider_code: str) -> dict:
    """Fetch service provider bank details from API"""
    try:
        params = {"provider_code": provider_code}
        url = f"{settings.BASE_URL}/menu/service-provider-bank"
        
        logger.info(f"Fetching provider bank details for: '{provider_code}'")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            logger.debug(f"Request URL: {response.url}")
            logger.debug(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.warning(f"Non-200 response for provider bank: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        logger.exception(f"Error fetching service provider bank details: {e}")
        return None


async def get_villa_bank_details(provider_code: str) -> dict:
    """Fetch villa bank details from API"""
    try:
        params = {"provider_code": provider_code}
        url = f"{settings.BASE_URL}/menu/villa-bank"
        
        logger.info(f"Fetching villa bank details for: '{provider_code}'")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            logger.debug(f"Request URL: {response.url}")
            logger.debug(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.warning(f"Non-200 response for villa bank: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        logger.exception(f"Error fetching villa bank details: {e}")
        return None


async def get_price_distribution(service_item: str) -> dict:
    """Fetch price distribution for service item"""
    try:
        params = {"service_item": service_item}
        url = f"{settings.BASE_URL}/menu/price_distribution"
        
        logger.info(f"Fetching price distribution for: '{service_item}'")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            logger.debug(f"Request URL: {response.url}")
            logger.debug(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.warning(f"Non-200 response for price distribution: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        logger.exception(f"Error fetching price distribution: {e}")
        return None

# Enhanced payment creation function
async def create_xendit_payment_with_distribution(order: Order):
    """Create payment invoice and prepare distribution data"""
    try:
        if not _set_xendit_api_key():
            return {
                'success': False,
                'error': 'XENDIT_SECRET_KEY is not configured'
            }

        price_distribution = await get_price_distribution(order.service_name)
        service_provider_bank = await get_service_provider_bank_details(order.service_provider_code) if order.service_provider_code else None
        villa_bank = await get_villa_bank_details(order.villa_code) if order.villa_code else None
        
        external_id = f"booking_{order.order_number}_{int(datetime.datetime.now().timestamp())}"
        
        try:
            price_clean = clean_price_string(order.price)
        except ValueError as e:
            logger.error(f"Price cleaning error for order {order.order_number}: {e}")
            return {
                'success': False,
                'error': f"Invalid price format: {order.price}"
            }

        distribution_data = None
        distribution_warning = None
        if price_distribution and service_provider_bank and villa_bank:
            try:
                service_provider_price = clean_price_string(price_distribution['service_provider_price'])
                villa_price = clean_price_string(price_distribution['villa_price'])
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
            except Exception as dist_err:
                distribution_warning = f"Split distribution unavailable: {dist_err}"
                logger.warning(f"{distribution_warning} (order {order.order_number})")
        else:
            distribution_warning = "Split distribution unavailable: missing price-distribution or bank details"
            logger.warning(
                f"{distribution_warning} for order {order.order_number} "
                f"(service_provider_code={order.service_provider_code}, villa_code={order.villa_code})"
            )
        
        # Create API client and instance
        api_client = xendit.ApiClient()
        api_instance = InvoiceApi(api_client)

        description_date = order.date.strftime('%d-%m-%Y') if order.date else "selected date"
        customer_name = order.name or "Customer"
        customer_mobile = order.phone_number or order.sender_id
        
        # Create invoice request
        create_invoice_request = CreateInvoiceRequest(
            external_id=external_id,
            amount=float(price_clean),
            currency='IDR',
            invoice_duration=86400.0,  # 24 hours in seconds
            description=f"Payment for {order.service_name} on {description_date} at {order.time}",
            customer=CustomerObject(
                given_names=customer_name,
                mobile_number=customer_mobile,
            ),
            customer_notification_preference=NotificationPreference(
                invoice_created=[NotificationChannel("whatsapp")],
                invoice_reminder=[NotificationChannel("whatsapp")],
                invoice_paid=[NotificationChannel("whatsapp")]
            ),
            success_redirect_url=f"{settings.WEB_BASE_URL}/chatbot",
            failure_redirect_url=f"{settings.WEB_BASE_URL}/payment-failed?order={order.order_number}",
            webhook_url=_resolve_xendit_webhook_url(),
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
        
        return {
            'success': True,
            'invoice_id': api_response.id,
            'payment_url': api_response.invoice_url,
            'external_id': external_id,
            'expires_at': api_response.expiry_date,
            'distribution_data': distribution_data,
            'distribution_warning': distribution_warning
        }
        
    except xendit.XenditSdkException as e:
        logger.exception(f"Xendit SDK Error for order {order.order_number}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        logger.exception(f"Xendit Invoice Creation Error for order {order.order_number}: {str(e)}")
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
        logger.exception(f"Database update error for order {order_number}: {str(e)}")
        return False
    

async def create_bank_disbursement(client: httpx.AsyncClient, amount: int, bank_details: dict, reference_id: str, description: str):
    try:
        if not _set_xendit_api_key():
            return {"success": False, "error": "XENDIT_SECRET_KEY is not configured"}

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
        logger.debug(f"Bank code type: {type(bank_code)}")

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
        logger.error(f"HTTP Error during disbursement: {e.response.text}")
        return {"success": False, "error": e.response.text}
    except Exception as e:
        logger.exception(f"Disbursement creation error: {str(e)}")
        return {"success": False, "error": str(e)}
    

async def distribute_order_payments(order_number: str, distribution_data: dict, retry_count: int = 0):
    """Distribute payments with automatic retry on failure (max 3 attempts)"""
    MAX_RETRIES = 3
    RETRY_DELAYS = [2, 4, 8]  # Exponential backoff in seconds
    
    try:
        if not _should_distribute_payments():
            logger.info(
                f"Skipping disbursements for order {order_number}: "
                "XENDIT_ENABLE_DISBURSEMENT is disabled"
            )
            await order_collection.update_one(
                {"order_number": order_number},
                {
                    "$set": {
                        "payment.disbursements": {
                            "skipped": True,
                            "reason": "XENDIT_ENABLE_DISBURSEMENT disabled",
                            "skipped_at": datetime.datetime.now()
                        },
                        "status": "payment_completed"
                    }
                }
            )
            return

        logger.info(f"Distributing payments for order {order_number} (attempt {retry_count + 1}/{MAX_RETRIES})")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            sp_result = await create_bank_disbursement(
                client=client,
                amount=distribution_data['service_provider']['amount'],
                bank_details=distribution_data['service_provider']['bank_details'],
                reference_id=f"sp_{order_number}_{retry_count}",
                description=f"Service provider payment for order {order_number}"
            )
            villa_result = await create_bank_disbursement(
                client=client,
                amount=distribution_data['villa']['amount'],
                bank_details=distribution_data['villa']['bank_details'],
                reference_id=f"villa_{order_number}_{retry_count}",
                description=f"Villa commission for order {order_number}"
            )
            
            # Track successful distribution
            await order_collection.update_one(
                {"order_number": order_number},
                {
                    "$set": {
                        "payment.disbursements": {
                            "service_provider": sp_result,
                            "villa": villa_result,
                            "distributed_at": datetime.datetime.now()
                        },
                        "payment.retry_count": retry_count,
                        "status": "funds_distributed"
                    },
                    "$push": {
                        "payment.retry_history": {
                            "attempt": retry_count + 1,
                            "status": "success",
                            "timestamp": datetime.datetime.now()
                        }
                    }
                }
            )
            
            logger.info(f"Payments distributed successfully for order {order_number}")
            
    except Exception as e:
        logger.error(f"Distribution error (attempt {retry_count + 1}/{MAX_RETRIES}) for order {order_number}: {str(e)}")
        
        # Record failure attempt
        await order_collection.update_one(
            {"order_number": order_number},
            {
                "$set": {
                    "payment.distribution_error": str(e),
                    "payment.retry_count": retry_count,
                    "status": "distribution_failed" if retry_count >= MAX_RETRIES - 1 else "distribution_retrying"
                },
                "$push": {
                    "payment.retry_history": {
                        "attempt": retry_count + 1,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.datetime.now()
                    }
                }
            }
        )
        
        # Retry with exponential backoff if attempts remaining
        if retry_count < MAX_RETRIES - 1:
            delay = RETRY_DELAYS[retry_count]
            logger.info(f"Retrying distribution for order {order_number} in {delay}s...")
            await asyncio.sleep(delay)
            return await distribute_order_payments(order_number, distribution_data, retry_count + 1)
        else:
            logger.error(f"Max retries ({MAX_RETRIES}) reached for order {order_number}. Manual intervention required.")
