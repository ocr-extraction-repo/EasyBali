from app.services.openai_client import client
from app.services.pinconeservice import get_index
from app.utils.chat_memory import get_conversation_history, save_message, trim_history
from app.services.ai_menu_generator import ai_menu_generator
from app.settings.config import settings
from typing import Dict, Any, Optional
import traceback


# ============================================================================
# PROFESSIONAL AI PERSONALITY (for non-menu responses only)
# ============================================================================

EASYBALI_CORE_IDENTITY = """You are the EASYBali AI Concierge — a sophisticated, warm, and knowledgeable digital assistant for luxury villa guests in Bali.

YOUR PERSONALITY:
- Warm and personable, like talking to a knowledgeable friend who's a Bali insider
- Professional but conversational (never robotic or scripted)
- Enthusiastic about helping without being over-the-top
- Attentive to details: you listen, remember, and anticipate needs
- Proactive: you suggest experiences, not just answer questions

YOUR COMMUNICATION STYLE:
- Natural, flowing conversation
- Paint pictures of experiences (not just list features)
- Ask clarifying questions when helpful
- Acknowledge emotions and context
- Always end with a clear next step or invitation to continue

YOUR EXPERTISE:
You know EASYBali services inside-out:
- Health & Wellness: Massage, IV drip therapy, yoga, Muay Thai, kickboxing, physiotherapy
- Transportation: Airport transfers, private drivers, tours, fast boats to Nusa Penida/Lembongan
- Villa Experiences: Private chef, movie night setups, shisha rental, gaming equipment (PS5, VR)
- Extra Services: Flowers, private barber, laundry pickup

You understand Bali logistics:
- Timing: massage needs 2-3hrs notice, private chef 24hrs, airport pickup same-day usually fine
- Pricing: varies by location (Seminyak cheaper than Uluwatu), group size, and service complexity
- Insider tips: best times for tours, what guests love most, how to avoid crowds"""


def _format_conversation_history(history: list) -> str:
    """Format conversation history for better context."""
    if not history:
        return "(First message from guest)"
    
    formatted = []
    for msg in history[-6:]:  # Last 6 messages for context
        role = "Guest" if msg["role"] == "user" else "You"
        formatted.append(f"{role}: {msg['content']}")
    
    return "\n".join(formatted)


def _clean_ai_response(text: str) -> str:
    """Remove AI artifacts and formatting issues."""
    text = text.strip()
    
    # Remove surrounding quotes
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        text = text[1:-1].strip()
    
    # Remove common AI prefixes
    prefixes = ["Here's my response:", "My response:", "Response:", "Here's what I'd say:", "I'd say:"]
    for prefix in prefixes:
        if text.lower().startswith(prefix.lower()):
            text = text[len(prefix):].strip()
    
    return text


async def whatsapp_response(query: str, user_id: str) -> Dict[str, Any]:
    try:
        service_check = await ai_menu_generator.intelligent_service_check(query)
    
        intent: Optional[Dict] = None
        requirements: Dict = ai_menu_generator.extract_requirements(query) or {}
        
        if service_check["we_offer_it"]:
            intent = ai_menu_generator.detect_service_intent(query)

            if not intent and service_check["matched_service"]:
                for service_type, info in ai_menu_generator.service_categories.items():
                    if info["subcategory"] == service_check["matched_service"]:
                        intent = {
                            "service_type": service_type,
                            "category": info["category"],
                            "subcategory": info["subcategory"]
                        }
                        break

        # Build intent info string
        intent_info = ""
        if intent and isinstance(intent, dict) and intent.get("category"):
            budget_str = (
                f"Under IDR {int(requirements.get('budget') or 0):,}"
                if requirements.get("budget")
                else "Any budget"
            )
            intent_info = f"""
DETECTED INTENT:
- Service: {intent.get('service_type', 'Unknown')}
- Category: {intent.get('category')}
- Subcategory: {intent.get('subcategory', 'Not specified')}
- Location: {requirements.get('location', 'Any area in Bali')}
- People: {requirements.get('people_count', 'Any')}
- Budget: {budget_str}
- Time: {requirements.get('time_preference', 'Flexible')}
""".strip()

        # Get chat history
        chat_history = get_conversation_history(user_id)
        conversation = trim_history(chat_history + [{"role": "user", "content": query}])

        # Get RAG context
        context = ""
        try:
            index = get_index("ai-data")
            embed = await client.embeddings.create(
                input=query,
                model="text-embedding-ada-002"
            )
            results = index.query(
                vector=embed.data[0].embedding,
                top_k=5,
                include_metadata=True
            )
            matches = results.get("matches", [])
            if matches:
                context_pieces = []
                for m in matches:
                    text = m.get("metadata", {}).get("text", "").strip()
                    score = m.get("score", 0)
                    if text and score > 0.75:
                        context_pieces.append(text)
                context = "\n\n".join(context_pieces)
        except Exception as e:
            print(f"[Pinecone] Non-critical error: {e}")

        will_show_menu = bool(intent and isinstance(intent, dict) and intent.get("category"))
        will_decline_service = (
            service_check["is_service_request"] and 
            not service_check["we_offer_it"] and
            service_check["confidence"] > 0.7
        )

        # ============================================================
        # RESPONSE PATH 1: Show menu (we have this service)
        # ============================================================
        if will_show_menu:
            general_examples = [
                '"Here are our available services. What would you like?"',
                '"Check out our services below"',
                '"Here\'s what we offer. Pick one to see details"',
            ]

            specific_examples = []
            if intent and intent.get("category"):
                loc = requirements.get("location")
                location_part = f" in {loc}" if loc else ""
                specific_examples = [
                    f'"Here are the available {intent["category"]} options{location_part}"',
                    f'"Check out our {intent.get("subcategory") or intent["category"]} services below"',
                    f'"Here are your {intent["category"].lower()} options"',
                ]

            all_examples = specific_examples + general_examples
            examples_block = "\n".join(f"- {ex}" for ex in all_examples[:3])

            prompt = f"""You are **EASYBali**, a helpful AI concierge for luxury villa guests in Bali.

Knowledge base context:
{context}

Recent conversation:
{conversation[-5:]}

{intent_info}

INSTRUCTIONS:
- Keep responses EXTREMELY short and simple (under 50 words)
- Just say "Here are the available options" or similar
- Be warm but concise
- Never be wordy or elaborate

STYLE EXAMPLES (match this simple tone):
{examples_block}

Now reply briefly:"""

            temperature = 0.5
            max_tokens = 80

        # ============================================================
        # RESPONSE PATH 2: Gracefully decline (unavailable service)
        # ============================================================
        elif will_decline_service:
            conversation_context = _format_conversation_history(conversation)
            
            requested_service_name = service_check.get("requested_service", "that service")
            
            prompt = f"""{EASYBALI_CORE_IDENTITY}

KNOWLEDGE BASE CONTEXT:
{context if context else "No specific service documentation needed."}

CONVERSATION HISTORY:
{conversation_context}

GUEST'S CURRENT MESSAGE: "{query}"

**CRITICAL INSTRUCTION**: The guest is asking about **{requested_service_name}**, which we DO NOT offer.

YOUR TASK:
1. Warmly acknowledge their request for {requested_service_name}
2. Briefly state we don't offer this service (don't apologize excessively)
3. Suggest 2-3 RELEVANT alternatives from our actual services that might interest them
4. Be helpful and solution-oriented

OUR AVAILABLE SERVICES (suggest from these):
- Health & Wellness: Massage, IV Drip, Yoga, Muay Thai, Boxing, Kickboxing, Physiotherapy
- Transportation: Airport Pickup/Drop, Private Driver Tours, Fast Boats to Islands
- Food & Beverage: Private Chef (breakfast, lunch, dinner, BBQ)
- Villa Experiences: Movie Night Setup, Shisha Rental
- Rentals: Gaming Equipment (PS5, VR), Projectors
- Extra Services: Private Barber, Flowers, Laundry

Keep response 80-120 words. Be warm, helpful, and offer clear alternatives.

YOUR RESPONSE:"""

            temperature = 0.8
            max_tokens = 180

        # ============================================================
        # RESPONSE PATH 3: Natural conversation (not service-related)
        # ============================================================
        else:
            conversation_context = _format_conversation_history(conversation)
            
            prompt = f"""{EASYBALI_CORE_IDENTITY}

KNOWLEDGE BASE CONTEXT (if relevant to guest's question):
{context if context else "No specific service documentation needed — use your general EASYBali knowledge."}

CONVERSATION HISTORY:
{conversation_context}

GUEST'S CURRENT MESSAGE: "{query}"

INSTRUCTIONS:
- Respond naturally and helpfully (this is a real conversation)
- Be warm, professional, and knowledgeable
- Paint experiences, don't just list facts
- Ask clarifying questions if helpful
- Suggest relevant services when appropriate
- End with clear next step or invitation
- Keep response 70-150 words (detailed but not overwhelming)

YOUR RESPONSE:"""

            temperature = 0.8
            max_tokens = 220

        # ========================================
        # Generate response
        # ========================================
        completion = await client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=0.3,
            frequency_penalty=0.3
        )
        ai_text = completion.choices[0].message.content.strip()
        ai_text = _clean_ai_response(ai_text)

        save_message(user_id, "user", query)
        save_message(user_id, "assistant", ai_text)

        # ========================================
        # Generate menu only if we have the service
        # ========================================
        menu_data = None
        should_send_menu = False
        image_url = None

        if intent and isinstance(intent, dict) and intent.get("category"):
            menu_data = await ai_menu_generator.generate_service_menu(
                category=intent["category"],
                subcategory=intent.get("subcategory"),
                requirements=requirements
            )
            should_send_menu = bool(menu_data and menu_data.get("sections"))
            
            if menu_data:
                image_url = menu_data.get("image_url")

        return {
            "text": ai_text,
            "image_url": image_url,
            "should_send_menu": should_send_menu,
            "menu_data": menu_data,
            "intent": intent or {},
            "requirements": requirements,
            "service_check": service_check  # For logging/analytics
        }

    except Exception as e:
        print(f"[whatsapp_response] Critical error: {e}")
        traceback.print_exc()
        
        return {
            "text": "Hi there! I'm your EASYBali concierge — here to help with in-villa spa & massage, private dining, transport, tours, and everything to make your stay incredible. What would you like to arrange today?",
            "image_url": None,
            "should_send_menu": False,
            "menu_data": None,
            "intent": {},
            "requirements": {},
            "service_check": None
        }