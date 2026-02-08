import json
import json
import httpx
from datetime import date
import datetime
from pydantic import BaseModel

from fastapi import HTTPException, Request, BackgroundTasks, Response
from fastapi import APIRouter
from app.settings.config import settings
from app.services.menu_services import get_main_menu_design, get_categories, get_categories_only, get_category_sections, get_service_items_for_whatsapp
from app.utils.whatsapp_func import process_message, send_whatsapp_service_flow_message
from app.models.chatbot_models import MenuRequest
from app.services.order_summary import active_chat_sessions
from app.routes.xendit_webhook import handle_xendit_webhook
from app.services.flow_encrytion import FlowCrypto

router = APIRouter(tags=["whatsapp"])


@router.get("/active-sessions")
async def get_active_sessions():
    sessions = {sender_id: order.dict() for sender_id, order in active_chat_sessions.items()}
    return sessions

@router.post("/main_design", summary="Get main menu items")
async def main_menu_design(request: MenuRequest):
    data = await get_main_menu_design()

    if "Menu Location" not in data.columns:
        raise HTTPException(status_code=500, detail="Invalid data format. Missing 'Menu Location' column.")
    filtered_data = data[data["Menu Location"] == request.type]

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail=f"No data found for menu type '{request.type}'")
    
    result = []
    for _, row in filtered_data.iterrows():
        result.append({
            "id":row["Title"].lower().replace(" ", "_"),
            "title": row["Title"],
            "picture": row["Picture"],
            "description": row["Description"],
            "button": row["Button"]
        })

    return {"data": result}

@router.get("/categories", summary="Get unique categories with description, picture, and button")
async def categories():
    try:
        return {"data": await get_categories()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/whatsapp-webhook")
async def verify_webhook(request: Request):
    try:
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")

        if mode == "subscribe" and token == settings.verify_token:
            return int(challenge)
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying webhook: {e}")

@router.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.json()
        print(f"🔍 DEBUG: Received webhook payload: {body}")

        entry = body.get("entry", [])
        if not entry:
            raise HTTPException(status_code=400, detail="No valid entry in request")
        
        for item in entry:
            changes = item.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])

                for message in messages:
                    sender_id = message.get("from")
                    message_id = message.get("id")
                    if not sender_id or not message_id:
                        continue  # Skip messages without sender ID
                    
                    # Extract message content
                    message_payload = {}
                    if "interactive" in message:
                        message_payload["interactive"] = message["interactive"]
                    elif "text" in message:
                        message_payload["text"] = message["text"]
                    
                    # Process message asynchronously
                    background_tasks.add_task(process_message, sender_id, message_payload, message_id)
        
        return {"status": "received"}

    except Exception as e:
        print(f"🚨 Error in webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Webhook error: {str(e)}")
    

@router.post("/webhook/xendit")
async def xendit_webhook_endpoint(request: Request):
    webhook_token = request.headers.get("x-callback-token")
    
    if webhook_token != "S9yCjrIxAogZgrfdiLXM7ePCR3dmZLjE3YFFleoQCFrWOSDf":
        raise HTTPException(status_code=401, detail="Unauthorized webhook")
    
    webhook_data = await request.json()
    await handle_xendit_webhook(webhook_data)
    return {"status": "success"}


try:
    PRIVATE_KEY_PASSWORD = settings.WHATSAPP_PRIVATE_KEY_PASSWORD
    if not PRIVATE_KEY_PASSWORD:
        print("⚠️  Warning: WHATSAPP_PRIVATE_KEY_PASSWORD environment variable not set")
        print("You can set it or modify the code to use a different method")
    
    crypto_handler = FlowCrypto(
        private_key_path="private.pem", 
        password=PRIVATE_KEY_PASSWORD
    )
    print("🚀 Crypto handler initialized successfully!")
    
except Exception as e:
    print(f"❌ Failed to initialize crypto handler: {e}")
    crypto_handler = None



#####################################################################

#############---- FLOW FOR SERVICE ITEMS SELECTION ---- #############

#####################################################################


SERVICES_DATA = [
    {
        "id": "1",
        "title": "Balinese Massage - 60min",
        "description": "Full body massage using oil cream to relax the body", 
        "metadata": "Rp 20,000"
    },
    {
        "id": "2", 
        "title": "Swedish Massage - 90min",
        "description": "Deep tissue massage for muscle relief",
        "metadata": "Rp 35,000"
    },
    {
        "id": "3",
        "title": "Hot Stone Therapy - 45min", 
        "description": "Relaxing hot stone treatment",
        "metadata": "Rp 25,000"
    },
    {
        "id": "4",
        "title": "Deep Tissue Massage - 75min", 
        "description": "Intensive muscle therapy for tension relief",
        "metadata": "Rp 30,000"
    },
    {
        "id": "5",
        "title": "Aromatherapy Session - 90min", 
        "description": "Essential oils massage for relaxation",
        "metadata": "Rp 40,000"
    },
    {
        "id": "6",
        "title": "Reflexology Treatment - 50min", 
        "description": "Foot massage therapy for wellness",
        "metadata": "Rp 18,000"
    }
]

def handle_init(data):
    """Handle combined booking flow initialization"""
    today = date.today()
    min_date = today.strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")
    flow_token = data.get("flow_token", "")
    
    print(f"🚀 Combined Booking Flow INIT - Token: {flow_token}, Today: {today_str}")
    
    return {
        "screen": "SERVICE_AND_DATE_SELECTION",
        "data": {
            "service_items": SERVICES_DATA,
            "min_date": min_date,
            "today_date": today_str,
            "flow_token": flow_token,
            "show_error": False,
            "error_message": ""
        }
    }

def handle_data_exchange(data):
    """Handle combined booking form submission"""
    screen_data = data.get("data", {})
    selected_service_id = screen_data.get("selected_service")
    selected_date = screen_data.get("selected_date")
    customer_name = screen_data.get("customer_name")
    customer_phone = screen_data.get("customer_phone")
    flow_token = data.get("flow_token", "")
    
    print(f"📋 Combined Booking DATA_EXCHANGE - Token: {flow_token}")
    print(f"🛍️ Service: {selected_service_id}")
    print(f"📅 Date: {selected_date}")
    print(f"👤 Name: {customer_name}")
    print(f"📞 Phone: {customer_phone}")
    print(f"📋 Full screen data: {screen_data}")
    
    # Validation
    errors = []
    
    # Validate service selection
    if not selected_service_id:
        errors.append("Please select a service")
    else:
        # Check if service exists
        selected_service = next(
            (service for service in SERVICES_DATA if service["id"] == selected_service_id),
            None
        )
        if not selected_service:
            errors.append("Invalid service selection")
    
    # Validate date
    if not selected_date:
        errors.append("Please select an appointment date")
    else:
        try:
            selected_date_obj = date.fromisoformat(selected_date)
            today_obj = date.today()
            
            if selected_date_obj < today_obj:
                errors.append("Please select a future date")
        except ValueError:
            errors.append("Invalid date format")
    
    # Validate customer name
    if not customer_name or len(customer_name.strip()) < 2:
        errors.append("Please enter a valid name (at least 2 characters)")
    
    # Validate phone number
    if not customer_phone or len(customer_phone.strip()) < 10:
        errors.append("Please enter a valid phone number")
    
    # If there are validation errors, return to form with errors
    if errors:
        today = date.today()
        print(f"❌ Validation errors: {errors}")
        return {
            "screen": "SERVICE_AND_DATE_SELECTION",
            "data": {
                "service_items": SERVICES_DATA,
                "min_date": today.strftime("%Y-%m-%d"),
                "today_date": today.strftime("%Y-%m-%d"),
                "flow_token": flow_token,
                "show_error": True,
                "error_message": " | ".join(errors)
            }
        }
    
    # All validations passed - get service details
    selected_service = next(
        (service for service in SERVICES_DATA if service["id"] == selected_service_id),
        None
    )
    
    selected_date_obj = date.fromisoformat(selected_date)
    
    print(f"✅ Booking confirmed successfully!")
    print(f"   Service: {selected_service['title']}")
    print(f"   Date: {selected_date_obj.strftime('%B %d, %Y')}")
    print(f"   Customer: {customer_name}")
    print(f"   Phone: {customer_phone}")
    
    # Complete the flow successfully with all booking data
    return {
        "screen": "SUCCESS",
        "data": {
            "extension_message_response": {
                "params": {
                    "flow_token": flow_token,
                    "selected_service": selected_service_id,
                    "selected_date": selected_date,
                    "customer_name": customer_name,
                    "customer_phone": customer_phone,
                    "service_title": selected_service["title"],
                    "service_description": selected_service["description"],
                    "service_price": selected_service["metadata"],
                    "formatted_date": selected_date_obj.strftime("%B %d, %Y"),
                    "status": "booking_completed"
                }
            }
        }
    }

def is_health_check_request(request_data: dict) -> bool:
    """
    Detect if the request is a health check from WhatsApp Manager.
    This avoids unnecessary decryption for pings/health probes.
    """
    if not isinstance(request_data, dict):
        return False

    # No encryption fields means it's not a real flow payload
    no_encryption_fields = not any(
        key in request_data for key in ["encrypted_flow_data", "encrypted_aes_key", "initial_vector"]
    )

    # Health check style indicators
    simple_structure = len(request_data.keys()) <= 3
    contains_health_keywords = any(
        key in request_data for key in ["health", "status", "ping", "timestamp"]
    )

    # Completely empty body is also a health check
    is_empty = len(request_data) == 0

    return no_encryption_fields and (is_empty or contains_health_keywords or simple_structure)

@router.post("/whatsapp-flow")
async def handle_flow(request: Request):
    """WhatsApp Flow endpoint for combined booking flow"""

    try:
        body = await request.body()
        print(f"📨 Received request, body length: {len(body)}")
        print(f"📨 Request headers: {dict(request.headers)}")

        if len(body) == 0:
            print("⚠️  Empty body received - returning OK")
            return Response(content="OK", status_code=200, media_type="text/plain")

        request_data = json.loads(body)
        print(f"📋 Request keys: {list(request_data.keys())}")
        print(f"📋 Full request data: {json.dumps(request_data, indent=2)}")

        encrypted_flow_data = request_data.get("encrypted_flow_data")
        encrypted_aes_key = request_data.get("encrypted_aes_key")
        initial_vector = request_data.get("initial_vector")

        print(f"🔍 DEBUG - Encrypted flow data: {encrypted_flow_data}")
        print(f"🔍 DEBUG - Encrypted AES key: {encrypted_aes_key}")
        print(f"🔍 DEBUG - Initial vector: {initial_vector}")

        if not crypto_handler:
            print("❌ Crypto handler not initialized")
            return Response(content="Crypto handler not initialized", status_code=500, media_type="text/plain")

        if not all([encrypted_flow_data, encrypted_aes_key, initial_vector]):
            missing = [x for x in ["encrypted_flow_data", "encrypted_aes_key", "initial_vector"]
                       if not request_data.get(x)]
            print(f"❌ Missing: {missing}")
            return Response(content=f"Missing: {missing}", status_code=400, media_type="text/plain")

        # 🔓 Decrypt
        try:
            print("🔓 Attempting to decrypt...")
            decrypted_data = crypto_handler.decrypt_request(
                encrypted_flow_data, encrypted_aes_key, initial_vector
            )

            if not decrypted_data:
                print("❌ Decryption returned None")
                return Response(content="Decryption returned None", status_code=500, media_type="text/plain")

        except Exception as e:
            print(f"❌ Decryption failed with error: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                content=f"Decryption failed: {str(e)}",
                status_code=500,
                media_type="text/plain"
            )

        print(f"✅ Decrypted data: {json.dumps(decrypted_data, indent=2)}")

        # 🎯 Handle actions
        action = decrypted_data.get("action", "UNKNOWN")
        version = decrypted_data.get("version", "UNKNOWN")
        flow_token = decrypted_data.get("flow_token", "UNKNOWN")

        print(f"🎬 Action: {action}, Version: {version}, Flow Token: {flow_token}")

        if action == "ping":
            print("🏓 Handling PING request")
            response_data = {
                "data": {
                    "status": "active"
                }
            }
        elif action == "INIT":
            print(f"🚀 Handling INIT request with token: {flow_token}")
            response_data = handle_init(decrypted_data)
        elif action == "data_exchange":
            print(f"📊 Handling DATA_EXCHANGE request")
            response_data = handle_data_exchange(decrypted_data)
        else:
            print(f"❓ Unknown action: {action}")
            response_data = {
                "screen": "ERROR",
                "data": {
                    "error": f"Unknown action: {action}"
                }
            }

        print(f"📤 Response data: {json.dumps(response_data, indent=2)}")

        # 🔐 Encrypt the response
        try:
            encrypted_response = crypto_handler.encrypt_response(response_data)
            if not encrypted_response:
                raise Exception("Encryption returned None")

            print(f"✅ Encrypted response length: {len(encrypted_response)}")
            print(f"🔍 Encrypted response sample: {encrypted_response[:100]}...")

            return Response(
                content=encrypted_response,
                media_type="text/plain",
                status_code=200
            )

        except Exception as enc_error:
            print(f"❌ Encryption failed: {enc_error}")
            return Response(
                content=f"Encryption failed: {str(enc_error)}",
                status_code=500,
                media_type="text/plain"
            )

    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return Response(
            content=f"JSON decode error: {str(e)}",
            status_code=400,
            media_type="text/plain"
        )
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return Response(
            content=f"Unexpected error: {str(e)}",
            status_code=500,
            media_type="text/plain"
        )



class TestFlowRequest(BaseModel):
    phone_number: str

@router.post("/test-flow")
async def test_flow_endpoint(request: TestFlowRequest):
    """Test endpoint to send combined booking flow to a specific WhatsApp number"""
    try:
        phone_number = request.phone_number.strip()
        
        # Basic phone number validation
        if not phone_number.isdigit() or len(phone_number) < 10:
            raise HTTPException(status_code=400, detail="Invalid phone number format. Use format: 923001234567")
        
        # Generate a test flow token for the combined booking flow
        test_flow_token = f"booking_{phone_number}_{int(datetime.datetime.now().timestamp())}"
        
        print(f"🧪 Testing combined booking flow for {phone_number} with token: {test_flow_token}")
        
        result = await send_whatsapp_service_flow_message(phone_number, test_flow_token)
        
        if result:
            return {
                "success": True,
                "message": f"Combined booking flow sent successfully to {phone_number}",
                "flow_token": test_flow_token,
                "flow_type": "combined_booking",
                "whatsapp_message_id": result.get('messages', [{}])[0].get('id', 'N/A'),
                "timestamp": datetime.datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send flow message")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Test flow error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    




###################################################################################

#############---- FLOW FOR CATEGORIES AND SUB-CATEGORY SELECTION ---- #############

###################################################################################

@router.get("/whatsapp_categories", summary="Get categories with title and description only")
async def categories_only():
    try:
        return {"categories": await get_categories_only()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/categories/sections", summary="Get sections for a specific category")
async def category_sections(request: dict):
    try:
        category_title = request.get("category_title")  # Changed
        if not category_title:
            raise HTTPException(status_code=400, detail="Category title is required in request body")
        return {"subcategories": await get_category_sections(category_title=category_title)}
    except ValueError as ve:
        if "not found" in str(ve):
            raise HTTPException(status_code=404, detail=str(ve))
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/sub_category/service_items", summary="Get service items for subcategory")
async def get_service_items(request:dict):
    try:
        # Change from subcategory_id to subcategory_title  
        subcategory_title = request.get("subcategory_title")  # Changed
        if not subcategory_title:
            raise HTTPException(status_code=400, detail="subcategory_title is required in request body")
        
        # Update your database query to use title instead of ID
        service_items = await get_service_items_for_whatsapp(subcategory_title=subcategory_title)
        return {"serviceitems": service_items}
    except ValueError as ve:
        if "not found" in str(ve):
            raise HTTPException(status_code=404, detail=str(ve))
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def fetch_categories():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://easy-bali.onrender.com/whatsapp_categories")
            if response.status_code == 200:
                data = response.json()
                categories = []
                for item in data.get("categories", []):
                    categories.append({
                        "id": item.get("title"),  # Use title as id
                        "main-content": {
                            "title": item.get("title"),
                            "metadata": item.get("description", "")
                        },
                        "on-click-action": {
                            "name": "data_exchange",
                            "payload": {
                                "selection": item.get("title")  # Pass title instead of id
                            }
                        }
                    })
                return categories
            else:
                print(f"API Error: {response.status_code}")
                return []
    except Exception as e:
        print(f"Failed to fetch categories: {e}")
        return []

async def fetch_subcategories(category_title: str):
    try:
        async with httpx.AsyncClient() as client:
            # Use category_title instead of category_id
            payload = {"category_title": category_title}  # Changed key name
            response = await client.post("https://easy-bali.onrender.com/categories/sections", json=payload)
            if response.status_code == 200:
                data = response.json()
                subcategories = []
                for item in data.get("subcategories", []):
                    subcategories.append({
                        "id": item.get("title"),  # Use title as id
                        "title": item.get("title"),
                        "description": item.get("description", ""),
                    })
                return subcategories
            else:
                print(f"API Error: {response.status_code}")
                return []
    except Exception as e:
        print(f"Failed to fetch subcategories: {e}")
        return []

async def fetch_service_items(subcategory_title: str):
    try:
        async with httpx.AsyncClient() as client:
            # Use subcategory_title instead of subcategory_id
            payload = {"subcategory_title": subcategory_title}  # Changed key name
            response = await client.post("https://easy-bali.onrender.com/sub_category/service_items", json=payload)
            if response.status_code == 200:
                data = response.json()
                service_items = []
                for item in data.get("serviceitems", []):
                    service_items.append({
                        "id": item.get("title"),  # Use title as id
                        "title": item.get("title"),
                        "description": item.get("description", ""),
                        "metadata": item.get("button", "")
                    })
                return service_items
            else:
                print(f"API Error: {response.status_code}")
                return []
    except Exception as e:
        print(f"Failed to fetch service items: {e}")
        return []

async def handle_category_flow_init(data):
    """Handle category flow initialization"""
    flow_token = data.get("flow_token", "")
    print(f"🚀 Category Flow INIT - Token: {flow_token}")
    
    # Fetch categories from API
    categories = await fetch_categories()
    
    return {
        "screen": "FIRST_SCREEN",
        "data": {
            "categories": categories
        }
    }


async def handle_category_flow_data_exchange(data):
    """Handle category flow data exchange - now handles 3 screens"""
    screen_data = data.get("data", {})
    selection = screen_data.get("selection")  # Category selection from screen 1
    subcategory_selection = screen_data.get("subcategory_selection")  # Subcategory selection from screen 2
    flow_token = data.get("flow_token", "")
    
    print(f"📋 Category Flow DATA_EXCHANGE - Token: {flow_token}")
    print(f"🏷️ Category Selection: {selection}")
    print(f"🏷️ Subcategory Selection: {subcategory_selection}")
    print(f"📋 Full screen data: {screen_data}")
    
    # Screen 1 -> Screen 2: User selected a category
    if selection and not subcategory_selection:
        print(f"📱 Moving to second screen for category: {selection}")
        
        # Fetch subcategories from API
        subcategories = await fetch_subcategories(selection)
        
        formatted_subcategories = []
        for subcategory in subcategories:
            formatted_subcategories.append({
                "id": subcategory["title"],
                "main-content": {
                    "title": subcategory["title"],
                    "metadata": subcategory["description"]
                },
                "on-click-action": {
                    "name": "data_exchange",
                    "payload": {
                        "selection": selection,  # Preserve the original category
                        "subcategory_selection": subcategory["title"],
                    }
                }
            })
        
        if formatted_subcategories:
            return {
                "screen": "SECOND_SCREEN",
                "data": {
                    "sub_categories": formatted_subcategories
                }
            }
        else:
            # No subcategories found, go back to first screen
            categories = await fetch_categories()
            return {
                "screen": "FIRST_SCREEN",
                "data": {
                    "categories": categories
                }
            }
    
    # Screen 2 -> Screen 3: User selected a subcategory
    elif subcategory_selection:
        print(f"📱 Moving to third screen (booking) for subcategory: {subcategory_selection}")
        print(f"📱 Original category: {selection}")
        
        # Fetch service items based on subcategory
        service_items = await fetch_service_items(subcategory_selection)
        
        if service_items:
            today = date.today()
            min_date = today.strftime("%Y-%m-%d")
            today_str = today.strftime("%Y-%m-%d")
            
            return {
                "screen": "SERVICE_AND_DATE_SELECTION",
                "data": {
                    "service_items": service_items,
                    "min_date": min_date,
                    "today_date": today_str,
                    "flow_token": flow_token,
                    "selected_category": selection,  # Now properly set
                    "selected_subcategory": subcategory_selection
                }
            }
        else:
            # No service items found, go back to subcategories for this category
            subcategories = await fetch_subcategories(selection)
            formatted_subcategories = []
            for subcategory in subcategories:
                formatted_subcategories.append({
                    "id": subcategory["title"],
                    "main-content": {
                        "title": subcategory["title"],
                        "metadata": subcategory["description"]
                    },
                    "on-click-action": {
                        "name": "data_exchange",
                        "payload": {
                            "selection": selection,
                            "subcategory_selection": subcategory["title"]
                        }
                    }
                })
            
            return {
                "screen": "SECOND_SCREEN",
                "data": {
                    "sub_categories": formatted_subcategories
                }
            }
    
    else:
        # Fallback to first screen
        print("⚠️ No valid selection found, returning to first screen")
        categories = await fetch_categories()
        return {
            "screen": "FIRST_SCREEN",
            "data": {
                "categories": categories
            }
        }

async def handle_category_flow_complete(data):
    """Handle category flow completion - simplified validation"""
    screen_data = data.get("data", {})
    selected_service = screen_data.get("selected_service")
    selected_date = screen_data.get("selected_date")
    calendar_date = screen_data.get("calendar")
    person_selection = screen_data.get("person_selection")
    time_selection = screen_data.get("time_selection")
    flow_token = data.get("flow_token", "")
    
    # Get the actual date value (calendar takes priority over selected_date)
    final_date = calendar_date if calendar_date else selected_date
    
    print(f"✅ Category Flow COMPLETE - Token: {flow_token}")
    print(f"🛍️ Selected service: {selected_service}")
    print(f"📅 Selected date: {final_date}")
    print(f"👥 Persons: {person_selection}")
    print(f"🕒 Time: {time_selection}")
    
    # Complete the booking without validation errors
    return {
        "data": {
            "extension_message_response": {
                "params": {
                    "flow_token": flow_token,
                    "selected_category": screen_data.get("selected_category", ""),
                    "selected_subcategory": screen_data.get("selected_subcategory", ""),
                    "selected_service": selected_service,
                    "selected_date": final_date,
                    "person_selection": person_selection,
                    "time_selection": time_selection,
                    "status": "booking_completed"
                }
            }
        }
    }
    

@router.post("/category-flow")
async def handle_category_flow(request: Request):
    """WhatsApp Category Flow endpoint"""

    try:
        body = await request.body()
        print(f"📨 Category Flow - Received request, body length: {len(body)}")
        print(f"📨 Request headers: {dict(request.headers)}")

        if len(body) == 0:
            print("⚠️  Empty body received - returning OK")
            return Response(content="OK", status_code=200, media_type="text/plain")

        request_data = json.loads(body)
        print(f"📋 Category Flow - Request keys: {list(request_data.keys())}")
        print(f"📋 Full request data: {json.dumps(request_data, indent=2)}")

        encrypted_flow_data = request_data.get("encrypted_flow_data")
        encrypted_aes_key = request_data.get("encrypted_aes_key")
        initial_vector = request_data.get("initial_vector")

        print(f"🔍 DEBUG - Encrypted flow data: {encrypted_flow_data}")
        print(f"🔍 DEBUG - Encrypted AES key: {encrypted_aes_key}")
        print(f"🔍 DEBUG - Initial vector: {initial_vector}")

        if not crypto_handler:
            print("❌ Category crypto handler not initialized")
            return Response(content="Category crypto handler not initialized", status_code=500, media_type="text/plain")

        if not all([encrypted_flow_data, encrypted_aes_key, initial_vector]):
            missing = [x for x in ["encrypted_flow_data", "encrypted_aes_key", "initial_vector"]
                       if not request_data.get(x)]
            print(f"❌ Missing: {missing}")
            return Response(content=f"Missing: {missing}", status_code=400, media_type="text/plain")

        # 🔓 Decrypt
        try:
            print("🔓 Attempting to decrypt category flow...")
            decrypted_data = crypto_handler.decrypt_request(
                encrypted_flow_data, encrypted_aes_key, initial_vector
            )

            if not decrypted_data:
                print("❌ Decryption returned None")
                return Response(content="Decryption returned None", status_code=500, media_type="text/plain")

        except Exception as e:
            print(f"❌ Decryption failed with error: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                content=f"Decryption failed: {str(e)}",
                status_code=500,
                media_type="text/plain"
            )

        print(f"✅ Decrypted category data: {json.dumps(decrypted_data, indent=2)}")

        # 🎯 Handle category actions
        action = decrypted_data.get("action", "UNKNOWN")
        version = decrypted_data.get("version", "UNKNOWN")
        flow_token = decrypted_data.get("flow_token", "UNKNOWN")

        print(f"🎬 Category Flow - Action: {action}, Version: {version}, Flow Token: {flow_token}")

        if action == "ping":
            print("🏓 Handling PING request for category flow")
            response_data = {
                "data": {
                    "status": "active"
                }
            }
        elif action == "INIT":
            print(f"🚀 Handling INIT request for category flow with token: {flow_token}")
            response_data = await handle_category_flow_init(decrypted_data)
        elif action == "data_exchange":
            print(f"📊 Handling DATA_EXCHANGE request for category flow")
            response_data = await handle_category_flow_data_exchange(decrypted_data)
        elif action == "complete":
            print(f"✅ Handling COMPLETE request for category flow")
            response_data = await handle_category_flow_complete(decrypted_data)
        else:
            print(f"❓ Unknown action in category flow: {action}")
            response_data = {
                "screen": "ERROR",
                "data": {
                    "error": f"Unknown action: {action}"
                }
            }

        print(f"📤 Category Flow Response data: {json.dumps(response_data, indent=2)}")

        # 🔐 Encrypt the response
        try:
            encrypted_response = crypto_handler.encrypt_response(response_data)
            if not encrypted_response:
                raise Exception("Encryption returned None")

            print(f"✅ Encrypted category response length: {len(encrypted_response)}")
            print(f"🔍 Encrypted response sample: {encrypted_response[:100]}...")

            return Response(
                content=encrypted_response,
                media_type="text/plain",
                status_code=200
            )

        except Exception as enc_error:
            print(f"❌ Encryption failed: {enc_error}")
            return Response(
                content=f"Encryption failed: {str(enc_error)}",
                status_code=500,
                media_type="text/plain"
            )

    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return Response(
            content=f"JSON decode error: {str(e)}",
            status_code=400,
            media_type="text/plain"
        )
    except Exception as e:
        print(f"💥 Unexpected error in category flow: {e}")
        import traceback
        traceback.print_exc()
        return Response(
            content=f"Unexpected error: {str(e)}",
            status_code=500,
            media_type="text/plain"
        )