from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from .security import hash_password, verify_password, create_access_token
from .auth import require_user

app = FastAPI(title="TST Identity Service (Dina)", version="1.0.0")

USERS: dict[str, dict] = {}

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

@app.get("/")
def root():
    return {
        "message": "Welcome to TST Identity Service (Dina)",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "register": "POST /auth/register",
            "login": "POST /auth/login",
            "me": "GET /auth/me",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "identity"}

@app.post("/auth/register")
def register(req: RegisterRequest):
    if req.username in USERS:
        raise HTTPException(status_code=400, detail="username already exists")
    USERS[req.username] = {"password_hash": hash_password(req.password), "role": req.role}
    return {"message": "registered", "username": req.username, "role": req.role}

@app.post("/auth/login")
def login(req: LoginRequest):
    u = USERS.get(req.username)
    if not u or not verify_password(req.password, u["password_hash"]):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_access_token(sub=req.username, role=u["role"])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me")
def me(payload=Depends(require_user)):
    return {"username": payload["sub"], "role": payload.get("role")}
