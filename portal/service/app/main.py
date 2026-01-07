from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .proxy import IDENTITY_BASE_URL, ATTENDANCE_BASE_URL, forward_json

app = FastAPI(title="TST Identity Portal (Dina)", version="1.0.0")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# Attendance Ratu public
@app.post("/api/checkins")
async def proxy_checkins(request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth} if auth else {}
    body = await request.json()
    return await forward_json("POST", f"{ATTENDANCE_BASE_URL}/checkins", headers=headers, json=body)

@app.get("/api/attendance/{event_id}")
async def proxy_attendance(event_id: str, request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth} if auth else {}
    return await forward_json("GET", f"{ATTENDANCE_BASE_URL}/attendance/{event_id}", headers=headers)

