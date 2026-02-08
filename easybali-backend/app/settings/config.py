from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str = "gpt-4o"
    whatsapp_api_url: str
    access_token: str
    verify_token: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_BUCKET_NAME:str
    AWS_REGION:str
    MONGO_URII:str
    pinecone_api_key : str
    pinecone_region : str
    pinecone_cloud : str
    XENDIT_SECRET_KEY:str
    BASE_URL:str
    WEB_BASE_URL:str
    WHATSAPP_APP_SECRET:str
    WHATSAPP_PRIVATE_KEY_PASSWORD:str

    class Config:
        env_file = ".env"


settings = Settings()