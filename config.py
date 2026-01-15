import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = 'regal_bank'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    FRAUD_THRESHOLD = 0.5
    BALANCE_CHECK = True