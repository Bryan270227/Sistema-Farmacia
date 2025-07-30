# auth/utils.py
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "tu_clave_secreta"  # Cambia esto por una clave segura

# Función para crear un token JWT
def create_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expira en 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Función para validar un token JWT
def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("Token inválido: falta user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")