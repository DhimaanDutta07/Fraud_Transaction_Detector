import secrets

def generate_token(length=32):
    return secrets.token_hex(length)