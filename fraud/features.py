import numpy as np
from joblib import load
from config import Config
import os

scaler = None

def load_scaler():
    global scaler
    scaler_path = 'models/scaler.pkl'
    if os.path.exists(scaler_path):
        scaler = load(scaler_path)
    return scaler

def scale_amount(amount):
    scaler = load_scaler()
    if scaler:
        return scaler.transform([[amount]])[0][0]
    return amount / 1000

def scale_time():
    from datetime import datetime
    hour = datetime.now().hour
    return (hour - 12) / 12

def generate_feature_vector(v_base, amount, time_scaled=None):
    if time_scaled is None:
        time_scaled = scale_time()
    
    amount_scaled = scale_amount(amount)
    feature_vector = v_base + [amount_scaled, time_scaled]
    return np.array(feature_vector, dtype=np.float32).reshape(1, -1)