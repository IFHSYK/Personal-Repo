import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

TOKEN = os.getenv('TELEGRAM_TOKEN')
