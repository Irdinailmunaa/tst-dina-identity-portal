# TUGAS 3: Ratu Attendance Service - API Analysis

## Overview
**Service Name:** TST Ratu Attendance Portal  
**Public URL:** https://ratu.theokaitou.my.id  
**Status:** ✅ Running on STB  
**Type:** Attendance Service + Portal Gateway  

## Architecture

Ratu's system is structured as:
```
┌────────────────────────────┐
│  Ratu Portal (UI Layer)    │ https://ratu.theokaitou.my.id
│  - Check-in interface      │
│  - Attendance management   │
└──────────┬─────────────────┘
           │
      ┌────┴─────┬──────────────┐
      │           │              │
      ▼           ▼              ▼
 ┌─────────┐ ┌──────────┐ ┌────────────┐
 │  Dina   │ │ Ratu     │ │ Event Mgt  │
 │Identity │ │Attendance│ │ Service    │
 └─────────┘ └──────────┘ └────────────┘
```

## API Endpoints

### 1. Health Check
**Endpoint:** `GET /health`  
**Authentication:** None  
**Response:**
```json
{
  "status": "ok",
  "service": "portal",
  "identity_base": "https://dina.theokaitou.my.id"
}
```

**Test Command:**
```bash
curl https://ratu.theokaitou.my.id/health -k
```

**Status:** ✅ Working

---

### 2. Authentication (Proxied from Dina Identity)

**GET /auth/me** - Get current user info
- **Authentication:** Required (Bearer token)
- **Headers:** `Authorization: Bearer <token>`
- **Response:** Current user information
- **Status:** ✅ Available

**POST /auth/login** - Login (via Dina)
- **Authentication:** None
- **Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:** Access token from Dina identity service
- **Status:** ✅ Available

**POST /auth/register** - Register (via Dina)
- **Authentication:** None
- **Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "role": "committee|admin"
  }
  ```
- **Response:** Registration confirmation
- **Status:** ✅ Available

---

### 3. Check-in Management

**POST /checkins** - Create check-in
- **Authentication:** Required (Bearer token from Dina)
- **Headers:** `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "event_id": "E001",
    "ticket_id": "T001"
  }
  ```
- **Response:** Check-in record
- **Expected Status:** ✅ Available
- **Test Command:**
  ```bash
  # 1. Register user
  curl -X POST https://ratu.theokaitou.my.id/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{
      "username": "petugas1",
      "password": "secure123",
      "role": "committee"
    }' -k
  
  # 2. Login to get token
  TOKEN=$(curl -s -X POST https://ratu.theokaitou.my.id/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{
      "username": "petugas1",
      "password": "secure123"
    }' -k | jq -r '.access_token')
  
  # 3. Create check-in
  curl -X POST https://ratu.theokaitou.my.id/api/checkins \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "event_id": "E001",
      "ticket_id": "T001"
    }' -k
  ```

---

### 4. Attendance Summary

**GET /attendance/{event_id}** - Get attendance for event
- **Authentication:** Required (Bearer token)
- **Headers:** `Authorization: Bearer <token>`
- **URL Parameters:** `event_id` (string)
- **Response:** Attendance records for the event
- **Expected Status:** ✅ Available
- **Test Command:**
  ```bash
  curl -H "Authorization: Bearer $TOKEN" \
    https://ratu.theokaitou.my.id/api/attendance/E001 -k
  ```

---

## Key Features

### 1. JWT Authentication
- **Shared Secret:** `RatuDinaTST2026_`
- **Algorithm:** `HS256`
- **Token Expiry:** 60 minutes
- **Issued By:** Dina Identity Service
- **Validated By:** Both Dina Portal and Ratu Attendance Service

### 2. Cross-Domain Integration
- Ratu proxies identity endpoints to Dina
- Ratu manages its own attendance data
- Token issued by Dina is valid on Ratu

### 3. Portal UI
- Check-in form with event_id and ticket_id
- Session management
- Login/Register interface
- Attendance display

---

## Testing Results

### Environment
- **Date:** 2026-01-08
- **Tested By:** TUGAS 3 Integration Analysis
- **Server:** Production STB

### Health Check Result
```
✅ Service is running
✅ Responding to requests
✅ Identity base URL configured correctly
✅ Ready for integration
```

---

## Integration Points for TUGAS 3

### Current Configuration (Already Updated)
In `.env.production` on STB:
```
IDENTITY_BASE_URL=https://dina.theokaitou.my.id
ATTENDANCE_BASE_URL=https://ratu.theokaitou.my.id
```

### Dina Portal Integration
Dina's Portal needs to:
1. ✅ Call `/api/auth/*` endpoints → proxies to IDENTITY_BASE_URL
2. ✅ Call `/api/checkins` endpoint → proxies to ATTENDANCE_BASE_URL
3. ✅ Call `/api/attendance/{event_id}` endpoint → proxies to ATTENDANCE_BASE_URL

### Current Status
- ✅ Configuration already updated for TUGAS 3
- ✅ Environment variables pointing to correct services
- ✅ JWT_SECRET and JWT_ALG already shared
- ⏳ Portal endpoints need to be exposed/tested
- ⏳ Integration testing needed

---

## Next Steps

1. **Test Portal Endpoints** - Verify Dina portal can call Ratu endpoints
2. **Create AttendanceClient** - Implement dedicated client in portal code
3. **Add /api/attendance/** endpoints - Expose Ratu data through Dina portal
4. **End-to-End Testing** - Test full integration flow
5. **Documentation** - Create complete API documentation

---

## Files & References

- **Ratu Repo:** (to be shared by partner)
- **Dina Portal Config:** `/opt/tst-dina-identity-portal/.env.production`
- **Docker Compose:** `/opt/tst-dina-identity-portal/docker-compose.prod.yml`
- **Portal Main:** `portal/service/app/main.py`
- **Portal Proxy:** `portal/service/app/proxy.py`

