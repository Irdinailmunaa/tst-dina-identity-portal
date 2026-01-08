# TUGAS 3: Architecture Design - Service Integration

## System Overview

### Current State (TUGAS 2)
```
┌─────────────────────────────────────────────┐
│      Dina Identity Portal (TUGAS 2)        │
│  Landing page + Identity management UI     │
│  (https://dina.theokaitou.my.id:18081)    │
└──────────────────┬──────────────────────────┘
                   │
            ┌──────▼──────────────┐
            │ Dina Identity Svc   │
            │ (register/login/me) │
            │ (Internal Docker)   │
            └─────────────────────┘
```

### TUGAS 3 - Enhanced Architecture
```
┌─────────────────────────────────────────────────────┐
│     Dina Identity Portal + Attendance Gateway       │
│  (TUGAS 2 + TUGAS 3 Integration)                   │
│  (https://dina.theokaitou.my.id:18081)            │
│                                                     │
│  Includes:                                         │
│  - Identity management (TUGAS 2)                  │
│  - Attendance integration (TUGAS 3)               │
│  - Admin/Committee panel                          │
│  - Check-in data from Ratu                        │
└──────────────┬──────────────────────────────────────┘
               │
       ┌───────┴────────────┬───────────────┐
       │                    │               │
       ▼                    ▼               ▼
  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐
  │   Dina      │  │    Ratu      │  │  External APIs  │
  │  Identity   │  │ Attendance   │  │  (Future)       │
  │    Svc      │  │    Svc       │  │                 │
  │ (Internal)  │  │ (Public API) │  │                 │
  └─────────────┘  └──────────────┘  └─────────────────┘
   register/login     checkins/
    /me endpoint     attendance
```

---

## Communication Flow

### 1. Authentication Flow
```
┌────────────┐
│   User     │
└─────┬──────┘
      │ 1. Login/Register
      ▼
┌─────────────────────────────────┐
│   Dina Portal                   │
│   /api/auth/login               │
│   /api/auth/register            │
└──────────┬──────────────────────┘
           │ 2. Proxy to Dina Identity
           ▼
┌──────────────────────────┐
│ Dina Identity Service    │
│ (Internal Docker)        │
│ - Verify credentials     │
│ - Issue JWT token        │
└──────────┬───────────────┘
           │ 3. Return JWT token
           │    (SECRET: RatuDinaTST2026_)
           │    (ALG: HS256)
           ▼
┌──────────────────────────┐
│   User (with token)      │
│   Ready for operations   │
└──────────────────────────┘
```

### 2. Attendance Query Flow
```
┌──────────────┐
│   User       │ (authenticated with Dina JWT token)
└──────┬───────┘
       │ 1. Request /api/attendance/E001
       ▼
┌──────────────────────────┐
│   Dina Portal            │
│   /api/attendance/E001   │
│   (NEW endpoint)         │
└──────┬───────────────────┘
       │ 2. Verify JWT token
       │    (validate signature with RatuDinaTST2026_)
       │
       │ 3. If valid, proxy to Ratu
       ▼
┌──────────────────────────┐
│   Ratu Attendance Svc    │
│   /api/attendance/E001   │
│   (Public URL)           │
└──────┬───────────────────┘
       │ 4. Return attendance data
       ▼
┌──────────────────────────┐
│   Dina Portal            │
│   (Format & return)      │
└──────┬───────────────────┘
       │ 5. Send to User
       ▼
┌──────────────────────────┐
│   User                   │
│   (sees attendance data) │
└──────────────────────────┘
```

### 3. Check-in Creation Flow
```
┌──────────────┐
│   Petugas    │ (committee/staff with JWT)
│   (Check-in) │
└──────┬───────┘
       │ 1. Form: event_id, ticket_id
       ▼
┌──────────────────────────┐
│   Dina Portal            │
│   POST /api/checkins     │
│   (NEW endpoint)         │
└──────┬───────────────────┘
       │ 2. Verify JWT token
       │    Extract user_id from token
       │
       │ 3. Proxy to Ratu with token
       ▼
┌──────────────────────────┐
│   Ratu Attendance Svc    │
│   POST /api/checkins     │
│   (Create check-in)      │
└──────┬───────────────────┘
       │ 4. Return check-in record
       ▼
┌──────────────────────────┐
│   Dina Portal            │
│   (Return success)       │
└──────┬───────────────────┘
       │ 5. Show confirmation
       ▼
┌──────────────────────────┐
│   Petugas                │
│   (See confirmation)     │
└──────────────────────────┘
```

---

## New Endpoints - Design

### Endpoint 1: Get Attendance Summary
```
GET /api/attendance/{event_id}

Purpose: Get attendance data for an event from Ratu

Headers:
  Authorization: Bearer <jwt_token_from_dina>
  Content-Type: application/json

URL Parameters:
  event_id: string (e.g., "E001")

Response (200 OK):
{
  "event_id": "E001",
  "event_name": "Tech Conference 2026",
  "total_registered": 150,
  "total_checked_in": 87,
  "checkin_percentage": 58,
  "checkins": [
    {
      "checkin_id": "C001",
      "ticket_id": "T001",
      "user_id": "user1",
      "checkin_time": "2026-01-08T10:30:00Z",
      "location": "Gate A"
    },
    ...
  ]
}

Response (401 Unauthorized):
{
  "detail": "Invalid or expired token"
}

Response (404 Not Found):
{
  "detail": "Event not found"
}
```

### Endpoint 2: Create Check-in
```
POST /api/checkins

Purpose: Create a new check-in record in Ratu

Headers:
  Authorization: Bearer <jwt_token_from_dina>
  Content-Type: application/json

Request Body:
{
  "event_id": "E001",
  "ticket_id": "T001"
}

Response (201 Created):
{
  "checkin_id": "C002",
  "event_id": "E001",
  "ticket_id": "T001",
  "user_id": "authenticated_user",
  "checkin_time": "2026-01-08T10:35:00Z",
  "status": "success"
}

Response (400 Bad Request):
{
  "detail": "Invalid ticket or already checked in"
}

Response (401 Unauthorized):
{
  "detail": "Invalid or expired token"
}

Response (404 Not Found):
{
  "detail": "Event or ticket not found"
}
```

### Endpoint 3: Get User Checkins (Optional)
```
GET /api/checkins?event_id=E001

Purpose: Get all check-ins for current user

Headers:
  Authorization: Bearer <jwt_token_from_dina>
  Content-Type: application/json

Query Parameters:
  event_id: string (optional, filter by event)

Response (200 OK):
{
  "user_id": "authenticated_user",
  "checkins": [
    {
      "checkin_id": "C001",
      "event_id": "E001",
      "event_name": "Tech Conference 2026",
      "ticket_id": "T001",
      "checkin_time": "2026-01-08T10:30:00Z"
    },
    ...
  ]
}

Response (401 Unauthorized):
{
  "detail": "Invalid or expired token"
}
```

---

## Implementation Components

### 1. AttendanceClient Class
**File:** `portal/service/app/attendance_client.py`

**Responsibilities:**
- Generate JWT tokens for Ratu API calls
- Make HTTP requests to Ratu endpoints
- Handle authentication errors
- Parse and return attendance data
- Implement retry logic and error handling

**Key Methods:**
- `__init__(base_url, jwt_secret, jwt_alg)` - Initialize client
- `get_token(user_id)` - Generate JWT for Ratu
- `get_attendance(event_id)` - GET /attendance/{event_id}
- `create_checkin(event_id, ticket_id)` - POST /checkins
- `get_user_checkins(user_id, event_id=None)` - GET /checkins

### 2. Portal Endpoints
**File:** `portal/service/app/main.py`

**New Endpoints:**
- `GET /api/attendance/{event_id}` - Proxy to Ratu
- `POST /api/checkins` - Proxy to Ratu
- `GET /api/checkins` - Proxy to Ratu (optional)

**Implementation Pattern:**
```
1. Extract JWT from request header
2. Verify JWT signature (using JWT_SECRET)
3. Extract user_id from JWT claims
4. Call AttendanceClient method with user_id
5. Catch errors and return appropriate HTTP status
6. Return response to client
```

### 3. Error Handling Strategy

**Errors to Handle:**
- Invalid/expired JWT → 401 Unauthorized
- Ratu service unavailable → 502 Bad Gateway
- Invalid event_id or ticket_id → 404 Not Found
- Duplicate check-in → 400 Bad Request
- Network timeout → 504 Gateway Timeout

---

## Security Considerations

### JWT Validation
```
✅ Token issued by Dina Identity Service
✅ Same secret (RatuDinaTST2026_) used for validation
✅ Algorithm: HS256
✅ Claims extracted: sub (user_id), exp (expiry), iat (issued at)
✅ Token expiry: 60 minutes
```

### Cross-Domain Access
```
✅ Ratu API is public (https://ratu.theokaitou.my.id)
✅ JWT token required for all operations
✅ Portal validates JWT before proxying to Ratu
✅ User context preserved in JWT claims
```

### Data Privacy
```
✅ Attendance data only accessible to authenticated users
✅ User_id extracted from JWT token (not from request body)
✅ Check-in operations attribute to authenticated user
✅ No sensitive data logged in HTTP responses
```

---

## Configuration

### Environment Variables (`.env.production`)
```
# Already configured:
IDENTITY_BASE_URL=https://dina.theokaitou.my.id
ATTENDANCE_BASE_URL=https://ratu.theokaitou.my.id
JWT_SECRET=RatuDinaTST2026_
JWT_ALG=HS256

# No changes needed - already points to Ratu!
```

### Docker Compose Changes
```yaml
# No changes needed to docker-compose.prod.yml
# Environment variables already read from .env.production
```

---

## Testing Strategy

### Unit Tests
```python
# Test AttendanceClient
- test_get_token() → verify JWT generation
- test_get_attendance() → verify API call
- test_create_checkin() → verify POST request
- test_error_handling() → verify exception handling
```

### Integration Tests
```bash
# 1. Authenticate
TOKEN=$(curl -X POST ... /api/auth/login | jq -r '.access_token')

# 2. Test attendance endpoint
curl -H "Authorization: Bearer $TOKEN" \
  /api/attendance/E001

# 3. Test check-in endpoint
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -d '{"event_id":"E001","ticket_id":"T001"}' \
  /api/checkins
```

### End-to-End Tests
```
1. User registers via Dina Portal
2. Gets JWT token
3. Calls /api/attendance/E001
4. Sees Ratu attendance data
5. Creates check-in via /api/checkins
6. Check-in appears in Ratu system
```

---

## Deployment Plan

### Phase 1: Code Implementation (Current)
- ✅ Design complete (Step 3)
- ⏳ Create AttendanceClient (Step 4)
- ⏳ Add endpoints to Portal (Step 5)
- ⏳ Local testing (Step 6)

### Phase 2: Deployment (Step 7)
- Verify `.env.production` on STB
- Rebuild portal-service Docker image
- Restart containers
- Verify endpoints accessible

### Phase 3: Integration Testing (Step 6)
- Test authentication flow
- Test attendance endpoint
- Test check-in creation
- Verify data from Ratu appears in Dina portal

---

## Benefits of this Design

✅ **Clean separation of concerns** - Dina focuses on identity, Ratu on attendance  
✅ **JWT-based security** - Shared token mechanism  
✅ **Stateless architecture** - No session affinity needed  
✅ **Easy scaling** - Services can scale independently  
✅ **Clear API contracts** - Well-defined endpoints  
✅ **Error handling** - Graceful error propagation  
✅ **Backward compatible** - TUGAS 2 functionality unchanged  

---

## Files to Modify

1. `portal/service/app/attendance_client.py` (NEW)
2. `portal/service/app/main.py` (MODIFY - add endpoints)
3. `docker-compose.prod.yml` (VERIFY - .env.production already updated)

---

## References

- JWT Specification: https://tools.ietf.org/html/rfc7519
- FastAPI Docs: https://fastapi.tiangolo.com
- HTTPX Client: https://www.python-httpx.org
- Ratu API: https://ratu.theokaitou.my.id/health
- Dina Identity: `http://identity-service:8000` (internal)

