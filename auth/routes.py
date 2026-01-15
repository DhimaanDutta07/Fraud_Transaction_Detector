from flask import Blueprint, request, jsonify
from db.mongo import get_db
import bcrypt
from schema import RegisterRequest, LoginRequest
import random

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        req = RegisterRequest(**data)
        db = get_db()
        
        if db.users_collection.find_one({'email': req.email}):
            return jsonify({'error': 'Email already registered'}), 400
        
        hashed_pwd = hash_password(req.password)
        v_base = [round(random.uniform(-1, 1), 2) for _ in range(28)]
        balance = round(random.uniform(2000, 10000), 2)
        avg_amount = round(random.uniform(50, 500), 2)
        
        user_doc = {
            'email': req.email,
            'password': hashed_pwd,
            'balance': balance,
            'v_base': v_base,
            'avg_amount': avg_amount,
            'tx_count': 0,
            'transactions': []
        }
        
        db.users_collection.insert_one(user_doc)
        return jsonify({'message': 'Registration successful', 'balance': balance}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        req = LoginRequest(**data)
        db = get_db()
        
        user = db.users_collection.find_one({'email': req.email})
        
        if not user or not verify_password(req.password, user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify({
            'message': 'Login successful',
            'email': user['email'],
            'balance': user['balance']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400