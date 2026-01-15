from pymongo import MongoClient
from config import Config

_db = None
_client = None

def init_mongo(app):
    global _db, _client
    try:
        _client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        _client.admin.command('ping')
        _db = _client[Config.DATABASE_NAME]
        _db.users_collection = _db['users']
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        _db = None

def get_db():
    global _db
    if _db is None:
        try:
            client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            _db = client[Config.DATABASE_NAME]
            _db.users_collection = _db['users']
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            return None
    
    _db.users_collection = _db['users']
    return _db
