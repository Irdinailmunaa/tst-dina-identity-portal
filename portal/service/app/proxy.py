import os
import httpx
from fastapi import Response

def _env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing environment variable: {name}")
    return v

IDENTITY_BASE_URL = _env("IDENTITY_BASE_URL").rstrip("/")
ATTENDANCE_BASE_URL = _env("ATTENDANCE_BASE_URL").rstrip("/")

async def forward_json(method: str, url: str, *, headers: dict | None = None, json: dict | None = None) -> Response:
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.request(method, url, headers=headers, json=json)
    return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("content-type","application/json"))
