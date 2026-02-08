import logging
from app.db.session import order_collection
from app.utils.whatsapp_func import notify_payment_completion
from app.services.payment_service import distribute_order_payments
from app.services.invoice_generator import generate_and_upload_invoice
from app.utils.whatsapp_func import send_invoice_and_handle_closure, send_whatsapp_message
from app.services.websocket_managerr import ConnectionManager
import datetime
import asyncio

manager= ConnectionManager()

logger = logging.getLogger(__name__)

async def handle_xendit_webhook(webhook_data: dict):
    try:
        logger.info(f"Xendit webhook received: {webhook_data}")

        if webhook_data.get("status") == "PAID":
            external_id = webhook_data.get("external_id")
            if not external_id or not external_id.startswith("booking_"):
                logger.warning(f"Invalid external_id format: {external_id}")
                return False
            
            order_number = external_id.split("_")[1]
            logger.info(f"Processing payment for order number: {order_number}")
            
            order_data = await order_collection.find_one({"order_number": order_number})
            if not order_data:
                logger.error(f"Order not found: {order_number}")
                return False
            
            # Prepare payment information
            payment_info = {
                "payment_status": "completed",
                "paid_at": datetime.datetime.now(),
                "payment_method": webhook_data.get("payment_method", "Online Payment"),
                "transaction_id": webhook_data.get("id"),
                "amount_paid": webhook_data.get("amount", order_data.get("price"))
            }
            
            # Update order with payment information
            await order_collection.update_one(
                {"order_number": order_number},
                {
                    "$set": {
                        "payment": {**order_data.get("payment", {}), **payment_info},
                        "status": "payment_completed"
                    }
                }
            )
            logger.info(f"Order {order_number} payment status updated to completed")

            # Generate and upload invoice
            logger.info(f"Generating invoice for order {order_number}")

            # Handle payment distribution
            distribution_data = order_data.get("payment", {}).get("distribution_data")
            if distribution_data:
                logger.info(f"Distributing payments for order {order_number}")
                try:
                    await distribute_order_payments(order_number, distribution_data)
                    logger.info(f"Payment distribution successful for order {order_number}")
                except Exception as dist_err:
                    logger.exception(f"Error during payment distribution for order {order_number}: {dist_err}")
            else:
                logger.warning(f"No distribution_data found for order {order_number}")

            # ============ ENHANCED: Support both WhatsApp and WebSocket ============
            # Determine connection type
            sender_id = order_data['sender_id']
            is_whatsapp = sender_id.isdigit()
            is_websocket = not is_whatsapp
            
            logger.info(f"Connection type for {sender_id}: {'WhatsApp' if is_whatsapp else 'WebSocket'}")

            # Send payment completion notification
            try:
                await notify_payment_completion(order_data)
                logger.info(f"Payment completion notification sent for order {order_number}")
            except Exception as notify_error:
                logger.exception(f"Error sending payment notification for order {order_number}: {notify_error}")
            
            # Generate invoice and handle final messaging
            try:
                invoice_result = await generate_and_upload_invoice(order_data, payment_info)
                
                if invoice_result['success']:
                    # Store invoice URL in database
                    await order_collection.update_one(
                        {"order_number": order_number},
                        {
                            "$set": {
                                "invoice.download_url": invoice_result['download_url'],
                                "invoice.generated_at": datetime.datetime.now(),
                                "invoice.invoice_data": invoice_result['invoice_data']
                            }
                        }
                    )
                    
                    # ============ ENHANCED: Send invoice with connection closure ============
                    await send_invoice_and_handle_closure(
                        order_data, 
                        invoice_result, 
                        is_whatsapp, 
                        is_websocket
                    )
                    logger.info(f"Invoice generated and sent for order {order_number}")
                    
                else:
                    logger.error(f"Invoice generation failed for order {order_number}: {invoice_result.get('error')}")
                    
            except Exception as invoice_error:
                logger.exception(f"Invoice generation error for order {order_number}: {invoice_error}")
                
            return True

        elif webhook_data.get("status") == "EXPIRED":
            external_id = webhook_data.get("external_id")
            if external_id and external_id.startswith("booking_"):
                order_number = external_id.split("_")[1]
                logger.info(f"Payment expired for order number: {order_number}")
                
                # Update order status to payment expired
                await order_collection.update_one(
                    {"order_number": order_number},
                    {
                        "$set": {
                            "payment.payment_status": "expired",
                            "payment.expired_at": datetime.datetime.now(),
                            "status": "payment_expired"
                        }
                    }
                )
                
                # ============ ENHANCED: Handle expired payments for both connections ============
                order_data = await order_collection.find_one({"order_number": order_number})
                if order_data:
                    await handle_payment_failure_or_expiry(
                        order_data, 
                        f"⏰ Payment link expired for order {order_number}. Please contact us to get a new payment link.",
                        "payment_expired"
                    )
                
                logger.info(f"Payment expiration handled for order {order_number}")
            return True

        elif webhook_data.get("status") == "FAILED":
            external_id = webhook_data.get("external_id")
            if external_id and external_id.startswith("booking_"):
                order_number = external_id.split("_")[1]
                logger.info(f"Payment failed for order number: {order_number}")
                
                # Update order status to payment failed
                await order_collection.update_one(
                    {"order_number": order_number},
                    {
                        "$set": {
                            "payment.payment_status": "failed",
                            "payment.failed_at": datetime.datetime.now(),
                            "status": "payment_failed",
                            "payment.failure_reason": webhook_data.get("failure_reason", "Unknown")
                        }
                    }
                )
                
                # ============ ENHANCED: Handle failed payments for both connections ============
                order_data = await order_collection.find_one({"order_number": order_number})
                if order_data:
                    await handle_payment_failure_or_expiry(
                        order_data, 
                        f"❌ Payment failed for order {order_number}. Please try again or contact us for assistance.",
                        "payment_failed"
                    )
                
                logger.info(f"Payment failure handled for order {order_number}")
            return True

        else:
            logger.info(f"Webhook status '{webhook_data.get('status')}' - no action required")
            return True

    except Exception as e:
        logger.exception(f"Webhook handling error: {str(e)}")
        return False
    

async def handle_payment_failure_or_expiry(order_data: dict, message: str, message_type: str):
    try:
        sender_id = order_data['sender_id']
        is_whatsapp = sender_id.isdigit()
        
        if is_whatsapp:
            await send_whatsapp_message(sender_id, message)
            
        else:
            await manager.send_personal_message(
                message=message,
                session_id=sender_id,
                message_type=message_type
            )
            
            # Close WebSocket connection after error
            await asyncio.sleep(0.5)
            await manager.send_personal_message(
                message="",
                session_id=sender_id,
                message_type="destroy"
            )
            
    except Exception as e:
        logger.exception(f"Payment failure/expiry handling error: {str(e)}")