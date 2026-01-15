from pymongo import MongoClient
from config import Config

_db = None
_client = None

def init_mongo(app):
    global _db, _client
    try:
        print(f"Connecting to MongoDB...")
        _client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=10000)
        _client.admin.command('ping')
        _db = _client[Config.DATABASE_NAME]
        print("✓ MongoDB connection successful!")
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        _db = None
        _client = None

def get_db():
    global _db, _client
    
    if _db is None:
        try:
            print("Attempting to reconnect to MongoDB...")
            _client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=10000)
            _client.admin.command('ping')
            _db = _client[Config.DATABASE_NAME]
            print("✓ MongoDB reconnected!")
        except Exception as e:
            print(f"✗ MongoDB reconnection failed: {e}")
            return None
    
    return _db

class DatabaseConnection:
    def __init__(self):
        self.users_collection = None
    
    def setup(self):
        db = get_db()
        if db is not None:
            self.users_collection = db['users']
        return self.users_collection is not None
