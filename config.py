import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI','mongodb://localhost:27017/').strip()
    DATABASE_NAME = 'Regal'
    SECRET_KEY = os.getenv('SECRET_KEY','your-secret-key-here').strip()
    FRAUD_THRESHOLD = 0.5
    BALANCE_CHECK = True
