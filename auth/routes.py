@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        req = RegisterRequest(**data)
        db = get_db()
        
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        users_collection = db['users']  
        
        if users_collection.find_one({'email': req.email}):
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
        
        users_collection.insert_one(user_doc)
        return jsonify({'message': 'Registration successful', 'balance': balance}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
