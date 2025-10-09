import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
LM_STUDIO_URL = os.getenv('LM_STUDIO_URL', 'http://localhost:1234/v1')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./poker_mentor.db')
AI_MODEL = os.getenv('AI_MODEL', 'deepseek-r1-distill-qwen-32b')

# Настройки покера
STARTING_CHIPS = 1500
BLINDS = [10, 20, 25, 50, 100, 200]