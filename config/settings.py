import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
LM_STUDIO_URL = os.getenv('LM_STUDIO_URL', 'http://localhost:1234/v1')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./poker_mentor.db')
AI_MODEL = os.getenv('AI_MODEL', 'qwen3-4b-2507')

# Настройки покера
STARTING_CHIPS = 1500
BLINDS = [10, 20, 25, 50, 100, 200]

# Настройки для Qwen
MAX_TOKENS = 512  # Уменьшаем для 4B модели
TEMPERATURE = 0.3  # Понижаем температуру для более консервативных ответов