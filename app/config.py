import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "Codefeast Smart Voice Agent"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Sarvam AI
    SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
    SARVAM_BASE_URL = os.getenv("SARVAM_BASE_URL", "https://api.sarvam.ai")
    
    # Internal Infrastructure
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://voiceadmin:voicepassword@localhost:5432/voice_agent_db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings()
