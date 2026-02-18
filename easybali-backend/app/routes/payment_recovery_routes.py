from fastapi import APIRouter, HTTPException
from app.services.payment_recovery import regenerate_payment_link, get_payment_recovery_options
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/payment/regenerate/{order_number}")
async def regenerate_payment_endpoint(order_number: str):
    """
    Regenerate payment link for failed/expired orders.
    
    Args:
        order_number: The order number to regenerate payment link for
        
    Returns:
        dict: Payment regeneration result with new payment_url
        
    Raises:
        HTTPException: 400 if regeneration not allowed, 500 for server errors
    """
    try:
        logger.info(f"Payment regeneration request received for order: {order_number}")
        result = await regenerate_payment_link(order_number)
        
        if not result.get("success"):
            logger.warning(f"Payment regeneration failed for {order_number}: {result.get('error')}")
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        logger.info(f"Payment regeneration successful for order: {order_number}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Payment regeneration endpoint error for {order_number}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/payment/recovery-options/{order_number}")
async def get_recovery_options_endpoint(order_number: str):
    """
    Get available recovery options for an order based on its payment status.
    
    Args:
        order_number: The order number to get recovery options for
        
    Returns:
        dict: Available recovery options including can_regenerate, can_retry, etc.
        
    Raises:
        HTTPException: 404 if order not found, 500 for server errors
    """
    try:
        logger.info(f"Recovery options request received for order: {order_number}")
        result = await get_payment_recovery_options(order_number)
        
        if not result.get("success"):
            logger.warning(f"Recovery options fetch failed for {order_number}: {result.get('error')}")
            raise HTTPException(status_code=404, detail=result.get("error"))
        
        logger.info(f"Recovery options fetched successfully for order: {order_number}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Recovery options endpoint error for {order_number}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
