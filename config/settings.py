import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
AI_MODEL = os.getenv("AI_MODEL")