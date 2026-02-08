import httpx
import json


from fastapi import HTTPException
from app.settings.config import settings
from app.services.openai_client import client
from app.utils.chat_memory import get_conversation_history, trim_history, save_message



async def language_lesson_ai(user_id: str) -> dict:
    try:
        chat_history = get_conversation_history(user_id)
        conversation = trim_history(chat_history)
        response = await client.responses.create(
            model=settings.OPENAI_MODEL_NAME,
            input=[
                {"role": "system", "content": (f"""You are a helpful Indonesian and Balinese language tutor. Your job is to create a lesson which includes: 1. Word, 2. Pronunciation, 3. Meaning in English, 4. Sentence in English and Indonesian. These are the previous lessons which you have generated {conversation} """)},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "language_lesson",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "word": {"type": "string"},
                            "pronounciation": {"type": "string"},
                            "Meaning": {"type": "string"},
                            "sentence": {"type": "string"},
                        },
                        "required": ["word", "pronounciation", "Meaning", "sentence"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )
        save_message(user_id, "assistant", response.output_text)
        lesson_data = json.loads(response.output_text)
        return lesson_data
    except json.JSONDecodeError:
        print("Failed to parse AI response")
        return None
    except Exception as e:
        print(f"Error generating lesson: {e}")
        return None

async def language_starting_message(recipient_number: str):
    try:
        lesson_data = await language_lesson_ai(recipient_number)
        if not lesson_data:
            raise ValueError("Failed to generate language lesson")
        lesson_text = (
            "Hi! Ready for your first language lesson of the day? Or feel free to ask us about any word or phrase you're curious about – We’re happy to help you with that too! 😊\n\n"
            "Today’s word/phrase is:\n\n"
            f"Word: {lesson_data['word']}\n"
            f"Pronunciation: {lesson_data['pronounciation']}\n"
            f"Meaning: {lesson_data['Meaning']}\n"
            f"Sentence: {lesson_data['sentence']}\n\n"
            "Would you like to learn more?"
        )

        headers = {
            "Authorization": f"Bearer {settings.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": lesson_text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {"id": "language_yes", "title": "✅ Yes"}
                        },
                        {
                            "type": "reply",
                            "reply": {"id": "language_no", "title": "❌ No"}
                        }
                    ]
                }
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(settings.whatsapp_api_url, json=payload, headers=headers)
            response.raise_for_status()

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    return response.json()




async def language_yes_message(recipient_number: str):
    try:
        lesson_data = await language_lesson_ai(recipient_number)
        if not lesson_data:
            raise ValueError("Failed to generate language lesson")
        lesson_text = (
            f"Word: {lesson_data['word']}\n"
            f"Pronunciation: {lesson_data['pronounciation']}\n"
            f"Meaning: {lesson_data['Meaning']}\n"
            f"Sentence: {lesson_data['sentence']}\n\n"
            "Would you like to learn more?"
        )

        headers = {
            "Authorization": f"Bearer {settings.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": lesson_text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {"id": "language_yes", "title": "✅ Yes"}
                        },
                        {
                            "type": "reply",
                            "reply": {"id": "language_no", "title": "❌ No"}
                        }
                    ]
                }
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(settings.whatsapp_api_url, json=payload, headers=headers)
            response.raise_for_status()

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    return response.json()



async def language_lesson_response(query: str, user_id: str):
    
    chat_history = get_conversation_history(user_id)
    conversation = trim_history(chat_history + [{"role": "user", "content": query}])

    prompt = f"""
    You are a friendly and knowledgeable local guide in Bali helping tourists learn useful Balinese and Indonesian phrases.
    Use the ongoing {conversation} history to maintain context, avoid repeating answers, and build on what the user has already learned.

    For each phrase or request from the user:
    - Provide the phrase in both Balinese and Indonesian (if different).
    - Include a phonetic pronunciation for both.
    - Give a brief explanation of when and how the phrase is used.
    - Maintain a warm, helpful, and culturally respectful tone, as if you're a patient local guide assisting a traveler.
    
    Do not use Markdown formatting like asterisks, hashtags, or symbols (e.g. *, #, -, etc.). Keep the formatting plain and simple for messaging apps like WhatsApp.
    Always assume the user is new to these languages, so avoid jargon. If they ask for general help (like greetings, restaurant terms, or customs), suggest common phrases tourists will find useful.

    Example question a user might ask:
    “How do I say 'thank you' in Balinese and Indonesian?”

    Example output:
    — Balinese: Suksma (pronounced: sooks-ma)
    — Indonesian: Terima kasih (pronounced: tuh-ree-mah kah-see)
    Use it after receiving help, like after someone serves you food or gives directions.
    """
    try:
        completion = await client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query},
            ],
            max_tokens=250,
            temperature=0.4,
        )

        response = completion.choices[0].message.content

        save_message(user_id, "user", query)
        save_message(user_id, "assistant", response)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {e}")
    


async def language_no_message(recipient_number: str):
    try:

        headers = {
            "Authorization": f"Bearer {settings.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "What would you like to do next?"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {"id": "language_phrase", "title": "💬 Phrases"}
                        },
                        {
                            "type": "reply", 
                            "reply": {"id": "back_to_menu", "title": "🔙 Main Menu"}
                        }
                    ]
                }
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(settings.whatsapp_api_url, json=payload, headers=headers)
            response.raise_for_status()

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    return response.json()