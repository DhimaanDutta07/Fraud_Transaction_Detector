import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email: str) -> bool:
    return '@' in email and '.' in email

def validate_password(password: str) -> bool:
    return len(password) >= 6