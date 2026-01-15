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
        
        # Get database connection
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        users_collection = db['users']
        
        # Check if email exists
        if users_collection.find_one({'email': req.email}):
            return jsonify({'error': 'Email already registered'}), 400
        
        # Hash password
        hashed_pwd = hash_password(req.password)
        
        # Generate user data
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
        
        # Insert user
        users_collection.insert_one(user_doc)
        print(f"✓ User registered: {req.email}")
        
        return jsonify({'message': 'Registration successful', 'balance': balance}), 201
    
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        req = LoginRequest(**data)
        
        # Get database connection
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        users_collection = db['users']
        
        # Find user
        user = users_collection.find_one({'email': req.email})
        
        if not user or not verify_password(req.password, user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        print(f"✓ User logged in: {req.email}")
        
        return jsonify({
            'message': 'Login successful',
            'email': user['email'],
            'balance': user['balance']
        }), 200
    
    except Exception as e:
        print(f"✗ Login error: {e}")
        return jsonify({'error': str(e)}), 400
