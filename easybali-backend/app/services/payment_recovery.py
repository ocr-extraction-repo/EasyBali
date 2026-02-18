import logging
import datetime
from app.db.session import order_collection
from app.services.payment_service import create_xendit_payment_with_distribution, update_order_with_payment_info
from app.utils.whatsapp_func import send_whatsapp_message
from app.models.order_summary import Order

logger = logging.getLogger(__name__)


async def regenerate_payment_link(order_number: str) -> dict:
    """
    Regenerate payment link for failed/expired orders.
    Returns new payment URL and invoice details.
    """
    try:
        order_data = await order_collection.find_one({"order_number": order_number})
        if not order_data:
            logger.error(f"Order not found for regeneration: {order_number}")
            return {"success": False, "error": "Order not found"}
        
        # Check if regeneration is allowed
        current_status = order_data.get("payment", {}).get("payment_status")
        if current_status not in ["failed", "expired"]:
            logger.warning(f"Regeneration blocked for order {order_number} with status: {current_status}")
            return {"success": False, "error": f"Cannot regenerate - current status: {current_status}"}
        
        # Convert to Order model
        order = Order(**order_data)
        
        # Create new payment invoice
        logger.info(f"Creating new payment invoice for order {order_number}")
        payment_result = await create_xendit_payment_with_distribution(order)
        
        if not payment_result.get("success"):
            logger.error(f"Payment creation failed during regeneration for order {order_number}: {payment_result.get('error')}")
            return payment_result
        
        # Update order with new payment info
        await update_order_with_payment_info(order_number, payment_result)
        
        # Track regeneration in history
        await order_collection.update_one(
            {"order_number": order_number},
            {
                "$push": {
                    "payment.regeneration_history": {
                        "regenerated_at": datetime.datetime.now(),
                        "previous_status": current_status,
                        "new_invoice_id": payment_result["invoice_id"],
                        "new_payment_url": payment_result["payment_url"]
                    }
                }
            }
        )
        
        logger.info(f"Payment link successfully regenerated for order {order_number}")
        return payment_result
        
    except Exception as e:
        logger.exception(f"Payment regeneration error for order {order_number}: {str(e)}")
        return {"success": False, "error": str(e)}


async def get_payment_recovery_options(order_number: str) -> dict:
    """
    Get available recovery options based on payment status.
    Returns current status and actionable options for user.
    """
    try:
        order_data = await order_collection.find_one({"order_number": order_number})
        if not order_data:
            logger.error(f"Order not found for recovery options: {order_number}")
            return {"success": False, "error": "Order not found"}
        
        payment_info = order_data.get("payment", {})
        status = payment_info.get("payment_status", "unknown")
        
        options = {
            "order_number": order_number,
            "current_status": status,
            "can_regenerate": status in ["failed", "expired"],
            "can_retry": False,
            "retry_attempts": payment_info.get("retry_count", 0),
            "max_retries": 3,
            "failure_reason": payment_info.get("failure_reason"),
            "payment_url": payment_info.get("payment_url")
        }
        
        # Check if payment is in retryable state
        if status in ["distribution_failed", "distribution_retrying"]:
            options["can_retry"] = options["retry_attempts"] < options["max_retries"]
        
        # Include regeneration history if exists
        if "regeneration_history" in payment_info:
            options["regeneration_count"] = len(payment_info["regeneration_history"])
        
        logger.info(f"Recovery options fetched for order {order_number}: {status}")
        return {"success": True, "options": options}
        
    except Exception as e:
        logger.exception(f"Error fetching recovery options for order {order_number}: {str(e)}")
        return {"success": False, "error": str(e)}
