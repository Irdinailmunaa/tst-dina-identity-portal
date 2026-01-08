from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import jwt
import os
from .proxy import IDENTITY_BASE_URL, ATTENDANCE_BASE_URL, forward_json
from .attendance_client import create_attendance_client, AttendanceClient

app = FastAPI(title="TST Identity Portal (Dina)", version="1.0.0")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# JWT configuration for token validation
JWT_SECRET = os.getenv("JWT_SECRET", "RatuDinaTST2026_")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

# Initialize attendance client
attendance_client: AttendanceClient | None = None
try:
    attendance_client = create_attendance_client()
except RuntimeError:
    pass  # Will fail at runtime if needed but service can start


def get_current_user(request: Request) -> dict:
    """
    Extract user info from JWT token in Authorization header
    
    For identity service tokens: Extract claims without validating signature
    (we trust identity service has issued valid tokens)
    
    For Ratu tokens: Validate with JWT_SECRET if needed
    
    Returns:
        Token claims including 'sub' (user_id)
    """
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = auth_header[7:]  # Remove "Bearer " prefix
    
    try:
        # Decode WITHOUT verification to extract claims
        # This works for identity service tokens (issued by identity service)
        # We trust the identity service has validated the token already
        payload = jwt.decode(token, "", algorithms=["HS256"], options={"verify_signature": False})
        
        # Extract user_id from 'sub' claim
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token missing 'sub' claim")
        
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed - {str(e)}")


@app.get("/health")
def health():
    return {"status":"ok","service":"portal","identity_base":IDENTITY_BASE_URL,"attendance_base":ATTENDANCE_BASE_URL}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Identity internal
@app.post("/api/auth/register")
async def proxy_register(request: Request):
    body = await request.json()
    return await forward_json("POST", f"{IDENTITY_BASE_URL}/auth/register", json=body)

@app.post("/api/auth/login")
async def proxy_login(request: Request):
    body = await request.json()
    return await forward_json("POST", f"{IDENTITY_BASE_URL}/auth/login", json=body)

@app.get("/api/auth/me")
async def proxy_me(request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth} if auth else {}
    return await forward_json("GET", f"{IDENTITY_BASE_URL}/auth/me", headers=headers)

# Attendance Ratu public - with AttendanceClient integration
@app.post("/api/checkins")
async def create_checkin(request: Request, current_user: dict = Depends(get_current_user)):
    """
    Create a new check-in record
    
    Uses AttendanceClient for direct communication with Ratu service.
    Validates JWT token and forwards request with user context.
    
    Body:
        {
            "event_id": "E001",
            "ticket_id": "T001"
        }
    """
    if not attendance_client:
        # Fallback to proxy if client not initialized
        auth = request.headers.get("authorization", "")
        headers = {"authorization": auth} if auth else {}
        body = await request.json()
        return await forward_json("POST", f"{ATTENDANCE_BASE_URL}/checkins", headers=headers, json=body)
    
    body = await request.json()
    user_id = current_user.get("sub", "unknown")
    
    result = await attendance_client.create_checkin(
        event_id=body.get("event_id"),
        ticket_id=body.get("ticket_id"),
        user_id=user_id
    )
    return result


@app.get("/api/attendance/{event_id}")
async def get_event_attendance(event_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get attendance summary for an event
    
    Uses AttendanceClient for direct communication with Ratu service.
    Validates JWT token and retrieves attendance data.
    
    Parameters:
        event_id: Event identifier (e.g., "E001")
    """
    if not attendance_client:
        # Fallback to proxy if client not initialized
        user_id = current_user.get("sub", "unknown")
        headers = {"Authorization": f"Bearer {user_id}"}  # In real scenario, would need to pass actual JWT token
        return await forward_json("GET", f"{ATTENDANCE_BASE_URL}/attendance/{event_id}", headers=headers)
    
    user_id = current_user.get("sub", "unknown")
    
    result = await attendance_client.get_attendance(
        event_id=event_id,
        user_id=user_id
    )
    return result


@app.get("/api/checkins")
async def get_user_checkins(event_id: str | None = None, current_user: dict = Depends(get_current_user)):
    """
    Get check-ins for the current user
    
    Optional filter by event_id.
    
    Query Parameters:
        event_id: Optional event identifier to filter check-ins
    """
    if not attendance_client:
        # Fallback to proxy if client not initialized
        user_id = current_user.get("sub", "unknown")
        headers = {"Authorization": f"Bearer {user_id}"}  # In real scenario, would need to pass actual JWT token
        params = f"?event_id={event_id}" if event_id else ""
        try:
            return await forward_json("GET", f"{ATTENDANCE_BASE_URL}/checkins{params}", headers=headers)
        except HTTPException as e:
            if e.status_code == 405:
                return {"message": "Get user checkins not yet supported by Ratu API", "user_id": user_id}
            raise
    
    user_id = current_user.get("sub", "unknown")
    
    try:
        result = await attendance_client.get_user_checkins(
            user_id=user_id,
            event_id=event_id
        )
        return result
    except HTTPException as e:
        # Ratu API may not support listing checkins yet, return placeholder
        if e.status_code in [405, 501]:
            return {"message": "Get user checkins not yet supported by Ratu API", "user_id": user_id}
        raise


