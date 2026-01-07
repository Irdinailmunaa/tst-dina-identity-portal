import os
import time
import bcrypt
import jwt

def _env(name: str, default: str | None = None) -> str:
    v = os.getenv(name, default)
    if v is None or v == "":
        raise RuntimeError(f"Missing environment variable: {name}")
    return v

JWT_SECRET = _env("JWT_SECRET")
JWT_ALG = _env("JWT_ALG")
TOKEN_EXPIRE_MINUTES = int(_env("TOKEN_EXPIRE_MINUTES", "60"))

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, pw_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), pw_hash.encode("utf-8"))

def create_access_token(sub: str, role: str) -> str:
    now = int(time.time())
    exp = now + TOKEN_EXPIRE_MINUTES * 60
    payload = {"sub": sub, "role": role, "iat": now, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])

