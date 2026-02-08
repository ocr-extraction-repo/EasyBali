from app.settings.config import settings
from fastapi import HTTPException
from app.services.menu_services import cache
from app.services.openai_client import client
from app.utils.chat_memory import get_conversation_history, trim_history, save_message
from app.services.pinconeservice import get_index
from app.utils.navigation_rules import rules

service_index="ai-data"


async def generate_response(query: str, user_id: str):
    index = get_index(service_index)
    chat_history = get_conversation_history(user_id)
    conversation = trim_history(chat_history + [{"role": "user", "content": query}])

    embed_response = await client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_vector = embed_response.data[0].embedding
    query_response = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )
    matches = query_response.get("matches", [])
    if not matches:
        context = ""
    else:
        context_chunks = [match["metadata"].get("text", "") for match in matches]
        context = "\n\n".join(context_chunks)
    prompt = f"""
        You are **easybali**, an AI concierge with access to a detailed service catalog (`{context}`) for villa guests in Bali.
        Respond to the {query} based on the context provided. 

        The conversation history (`{conversation}`), which stores the guest’s previous queries and your responses. Use it to maintain context and continuity in your replies.

        if query is related to booking use these {rules} to guide about how they can book a respective service.
    """
    try:
        completion = await client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query},
            ],
        )

        response = completion.choices[0].message.content
        save_message(user_id, "user", query)
        save_message(user_id, "assistant", response)

        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {e}")