import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    ALLOWED_USER_IDS = {562442831, 354135340, 222459211, 2028809889}
    