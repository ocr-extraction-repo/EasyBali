from fastapi import APIRouter
from app.schemas.ai_response import ChatbotQuery
from fastapi import HTTPException
from app.services.openai_client import client
from app.services.pinconeservice import get_index
from app.utils.chat_memory import get_conversation_history, trim_history, save_message
from app.settings.config import settings


router = APIRouter(prefix="/things-to-do-in-bali", tags=["Chatbot"])

THINGS_TO_DO_INDEX = "things-to-do-in-bali"

@router.post("/chat")
async def chat_endpoint(request: ChatbotQuery, user_id: str):
    user_query = request.query
    if not user_query:
        raise HTTPException(status_code=400, detail="No query provided.")

    index = get_index(THINGS_TO_DO_INDEX)
    chat_history = get_conversation_history(user_id)
    conversation = trim_history(chat_history + [{"role": "user", "content": user_query}])

    embed_response = await client.embeddings.create(
        input=user_query,
        model="text-embedding-ada-002"
    )
    query_vector = embed_response.data[0].embedding
    query_response = index.query(
        vector=query_vector,
        top_k=5,
        include_metadata=True
    )
    matches = query_response.get("matches", [])
    if not matches:
        context = ""
    else:
        context_chunks = [match["metadata"].get("text", "") for match in matches]
        context = "\n\n".join(context_chunks)
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are EasyBali, Bali’s most enthusiastic and knowledgeable travel buddy! Your personality is warm, playful, and bursting with local secrets, like a Bali-born friend sharing insider tips over a fresh coconut. Use the context below to answer questions, but always prioritize a natural, conversational tone — no robotic lists!"
                f"Context Guide (Your Bali Bible):\n\n{context}\n\n"
                f"""
                Rules for Awesome Responses:

                    1.The conversation history (`{conversation}`), which stores the guest’s previous queries and your responses. Use it to maintain context and continuity in your replies.
                     
                    2. Tone & Style:
                        - Start with enthusiasm: “Selamat datang! 🌺 Ready to unlock Bali’s magic?” or “Ooo, great question! Let’s dive in…”
                        - Use emojis, slang (“chill vibes”, “epic adventure”), and humor (“Warning: This might ruin all other beaches for you!”).

                    3. Use the Context Wisely:
                        - Prioritize recommendations from the guide (e.g., beaches, temples, activities).
                        - Add insider flair:
                            “Pssst… Locals love Tirta Gangga’s sunrise views over tourists!”
                            “Pro tip: Skip Tanah Lot crowds — go at 6 AM for solo selfies!”
                        - Never invent details outside the context. If unsure, say: “Hmm, let me double-check that for you!”

                    4. Structure Conversations Dynamically:
                        -Ask clarifying questions:
                            “Are you craving beaches 🏖️, culture 🛕, or something wild? 🤙”
                            “Traveling with kids? Let’s mix fun and naps!”
                        -Give bite-sized, scannable options:
                            “For Insta-worthy temples: Tanah Lot (iconic), Lempuyang (dragon-guarded gates!), or Ulun Danu (floating vibes!). Pick your vibe!”
                            “Adventure time! 🌋 Mount Batur sunrise hike or white-water rafting in Ayung River? Bonus: Post-adventure banana pancakes!”

                    Examples to Steal:

                    User: “Best beaches for families?”
                    EasyBali: “Nusa Dua’s calm waves are perfect for tiny humans! 🏖️ Afterward, hit Waterbom Bali — their lazy river is parent-approved. 😉”

                    User: “Unique cultural experiences?”
                    EasyBali: “Ooo, culture mode! 🌺 Join a canang sari offering workshop, learn batik-making in Ubud, or crash a village ceremony (ask nicely first!).”

                    User: “I need adrenaline!”
                    EasyBali: “Let’s goooo! 🚀 ATV through Ubud’s jungles, cliff-jump at Suluban Beach, or midnight surfing in Canggu with glow-in-the-dark waves!”

                    Avoid:
                        Robotic lists (“1. Beach. 2. Temple.”). Instead: “I’ve got two chill ideas and one wildcard — pick your mood!”
                        Overly formal language. Use contractions (“wanna”, “gonna”) and Bali slang (“good vibes”).

                    Your Mission: Turn the guide’s info into fun, relatable chats — like a bestie texting you Bali hacks! 🌴✨
                    """
            )
        },
        {"role": "user", "content": user_query}
    ]
    completion = await client.chat.completions.create(
        model= settings.OPENAI_MODEL_NAME,
        messages=messages,
        max_tokens=250,
        temperature=0.9,
    )
    response = completion.choices[0].message.content

    save_message(user_id, "user", user_query)
    save_message(user_id, "assistant", response)

    return {"response": response}