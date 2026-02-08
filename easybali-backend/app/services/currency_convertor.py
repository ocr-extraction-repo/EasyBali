from app.settings.config import settings
from app.services.openai_client import client
from app.utils.chat_memory import get_conversation_history, trim_history, save_message


async def currency_ai(user_id: str, query: str) -> dict:
    try:
        chat_history = get_conversation_history(user_id)
        conversation = trim_history(chat_history)
        response = await client.responses.create(
            model=settings.OPENAI_MODEL_NAME,
            tools=[{"type": "web_search_preview"}],
            input=[
                {"role": "system", "content": (f""" 
                                                You are an intelligent currency conversion assistant designed for tourists visiting Bali, Indonesia. Your task is to help users convert their home currency into Indonesian Rupiah (IDR) using the most recent exchange rates.
                                                The Response should always be in whatsapp Markdown format.
                                                Use the previous context to respond {conversation}.
                                                When a user provides a currency code or name (e.g., 'USD', 'Euro', 'Japanese Yen') and an amount, respond only with:

                                                 1- The converted value in IDR.

                                                 2- A brief sentence to help tourists understand the value in practical terms (e.g., 'This is enough for a mid-range dinner for two in Bali.')
                                                    Use accurate and current exchange rates. If the exchange rate is not available, politely let the user know. Do not guess.
                                                    Be friendly and helpful, like a local guide.
                                                """)},
                {"role": "user", "content": query}
            ],
        )
        save_message(user_id, "user", query)
        save_message(user_id, "assistant", response.output_text)
        return response.output_text
    

    except Exception as e:
        print(f"Error generating lesson: {e}")
        return None