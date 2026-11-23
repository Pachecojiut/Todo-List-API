import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

if not SECRET_KEY or len('SECRET_KEY') < 32:
    raise RuntimeError("SECRET_KEY ausente ou curta demais (mínimo 32 caracteres). "
        "Gere uma com: python -c \"import secrets; print(secrets.token_hex(32))\"")

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_token(user_id: int) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {'sub': str(user_id), 'exp': expiracao}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token: int) -> None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={'require': ['exp', 'sub']},
        )
        return int(payload['sub'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None



