from flask import Blueprint, request, jsonify
from db.mongo import get_db
from fraud.features import generate_feature_vector
from config import Config
import tensorflow as tf
import os

fraud_bp = Blueprint('fraud', __name__, url_prefix='/fraud')

model = None

def load_model():
    global model
    if model is not None:
        return model
        
    try:
        model_path = 'models/best_fraud_nn_model.keras'
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            return model
    except Exception:
        pass
    return None

@fraud_bp.route('/predict', methods=['POST'])
def predict_fraud():
    try:
        data = request.json
        email = data.get('email')
        amount = float(data.get('amount'))
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        user = db.users_collection.find_one({'email': email})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if amount > user['balance']:
            return jsonify({
                'status': 'rejected',
                'message': 'Insufficient balance',
                'confidence': 100,
                'balance': user['balance']
            }), 200
        
        current_model = load_model()
        
        v_base = user['v_base']
        feature_vector = generate_feature_vector(v_base, amount)
        
        if current_model:
            fraud_prob = float(current_model.predict(feature_vector, verbose=0)[0][0])
        else:
            fraud_prob = 0.15
        
        avg_amount = user.get('avg_amount', 300.0)
        
        if amount > avg_amount * 4:
            fraud_prob = min(fraud_prob + 0.55, 0.99)
        
        if amount > 5000:
            fraud_prob = min(fraud_prob + 0.30, 0.99)
        
        if amount > avg_amount * 2:
            fraud_prob = min(fraud_prob + 0.15, 0.99)
        
        effective_threshold = 0.38
        
        if fraud_prob > effective_threshold:
            return jsonify({
                'status': 'rejected',
                'message': 'Transaction flagged as suspicious',
                'confidence': round(fraud_prob * 100, 2),
                'balance': user['balance']
            }), 200
        
        new_balance = user['balance'] - amount
        db.users_collection.update_one(
            {'email': email},
            {
                '$set': {'balance': new_balance},
                '$push': {'transactions': amount},
                '$inc': {'tx_count': 1}
            }
        )
        
        return jsonify({
            'status': 'approved',
            'message': 'Transaction approved',
            'confidence': round((1 - fraud_prob) * 100, 2),
            'balance': new_balance
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400