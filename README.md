# Identity Service & Attendance Integration Portal TixGo

**TixGo** adalah sistem terintegrasi untuk identity management dan operational attendance portal yang terhubung dengan Ratu Attendance Service. Dikembangkan sebagai submission untuk **UAS II3160 Teknologi Sistem Terintegrasi**.

## Project Summary

| Tugas | Komponen | Status | Deskripsi |
|-------|----------|--------|-----------|
| TUGAS 2 | Identity Service | PRODUCTION READY | Core authentication service dengan JWT, user registration, login, dan token validation |
| TUGAS 3 | Identity Portal + Ratu Integration | DEPLOYMENT READY | Admin/Committee portal dengan integrated attendance check-in system dari Ratu |

### Fitur Utama
- User authentication dengan JWT (HS256)
- Role-based access control (admin, committee, user)
- Integrated attendance verification
- Real-time check-in management
- Microservices architecture
- Production-ready deployment

---

## Struktur Project

```
tst-dina-identity-portal/
├── identity/service/        # TUGAS 2: Identity Service (Core)
│   └── app/
│       ├── main.py         # Endpoints: /register, /login, /auth/me
│       ├── auth.py         # JWT token validation dependency
│       └── security.py     # Password hashing & JWT encode/decode
│
├── portal/service/          # TUGAS 3: Portal + Ratu Integration
│   ├── app/
│   │   ├── main.py         # Portal endpoints & routes
│   │   ├── proxy.py        # Proxy to identity & Ratu services
│   │   └── ratu_client.py  # Ratu API integration (future)
│   └── templates/          # HTML admin/inspector panel
│
├── TUGAS_2.md              # Tugas 2 Formal Document
├── MAKALAH.md              # Tugas 3 paper
├── ARCHITECTURE.md         # System design & flow
├── DEPLOYMENT.md           # Step-by-step deployment
├── docker-compose.yml      # Development setup
├── docker-compose.prod.yml # Production setup
└── README.md               # This file
```

---

## CARA AKSES LAYANAN

### Akses dari Browser (Recommended)

#### 1. Portal Identity (Identity + Attendance Integration)
```
URL: https://dina.theokaitou.my.id
Port: 443 (HTTPS)
Status: Public (via Cloudflare Tunnel)
```

**Fitur yang tersedia:**
- User Registration & Login
- Dashboard dengan attendance overview
- Check-in verification
- Attendance statistics

**Default Credentials untuk Testing:**
```
Username: admin
Password: admin123
Role: admin
```

**Atau register user baru:**
1. Click "Masuk" → Tab "Register"
2. Isi username, password, role
3. Click "Register"
4. Login dengan credentials baru

#### 2. Ratu Attendance Service (Partner)
```
URL: https://ratu.theokaitou.my.id
Port: 443 (HTTPS)
Status: Public
```

**Fitur:**
- Event management
- Attendance tracking
- Check-in QR code scanning

### Akses dari Terminal (API Testing)

#### Development Environment
```bash
# Identity Service
IDENTITY_URL="http://localhost:18080"

# Portal Service
PORTAL_URL="http://localhost:18081"

# Ratu Attendance (if local)
RATU_URL="http://localhost:18082"
```

#### Production Environment (STB)
```bash
# Via SSH
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id

# Then test from STB
curl -s http://localhost:18081/health | jq .
```

#### Public Access (Cloudflare Tunnel)
```bash
# Identity Service (proxied through Portal)
curl https://dina.theokaitou.my.id/api/auth/register

# Ratu Attendance
curl https://ratu.theokaitou.my.id/health
```

---

## QUICK START

### Development Setup

```bash
# Clone repository
git clone https://github.com/Irdinailmunaa/tst-dina-identity-portal.git
cd tst-dina-identity-portal

# Start all services (identity + portal + database)
docker-compose up -d --build

# Verify services running
docker-compose ps

# Check health endpoints
curl http://localhost:18081/health | jq .
curl http://localhost:18080/health | jq .
```


### API Examples (Curl Commands)

#### Health Check
```bash
curl -s http://localhost:18080/health | jq .
# Response: {"status":"ok","service":"identity"}
```

#### Register New User
```bash
curl -X POST http://localhost:18080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123",
    "role": "user"
  }' | jq .

# Response:
# {
#   "message": "registered",
#   "username": "testuser",
#   "role": "user"
# }
```

#### Login (Get JWT Token)
```bash
curl -X POST http://localhost:18080/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }' | jq .

# Response:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }
```

#### Use Token to Get User Info (Protected Endpoint)
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET http://localhost:18080/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq .

# Response:
# {
#   "username": "testuser",
#   "role": "user"
# }
```

#### Complete Test Flow
```bash
#!/bin/bash

# 1. Register
echo "=== REGISTER ==="
REG=$(curl -s -X POST http://localhost:18080/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123","role":"admin"}')
echo $REG | jq .

# 2. Login
echo -e "\n=== LOGIN ==="
LOGIN=$(curl -s -X POST http://localhost:18080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}')
echo $LOGIN | jq .
TOKEN=$(echo $LOGIN | jq -r '.access_token')

# 3. Use token
echo -e "\n=== GET USER INFO ==="
curl -s -X GET http://localhost:18080/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq .

# 4. Try invalid token
echo -e "\n=== INVALID TOKEN (should fail) ==="
curl -s -X GET http://localhost:18080/auth/me \
  -H "Authorization: Bearer invalid_token" | jq .
#### Complete Test Flow
```bash
#!/bin/bash

# 1. Register
echo "=== REGISTER ==="
REG=$(curl -s -X POST http://localhost:18080/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123","role":"admin"}')
echo $REG | jq .

# 2. Login
echo -e "\n=== LOGIN ==="
LOGIN=$(curl -s -X POST http://localhost:18080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}')
echo $LOGIN | jq .
TOKEN=$(echo $LOGIN | jq -r '.access_token')

# 3. Use token
echo -e "\n=== GET USER INFO ==="
curl -s -X GET http://localhost:18080/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq .

# 4. Try invalid token
echo -e "\n=== INVALID TOKEN (should fail) ==="
curl -s -X GET http://localhost:18080/auth/me \
  -H "Authorization: Bearer invalid_token" | jq .
```

---

## TUGAS 3: Identity Portal + Attendance Integration

### Portal Endpoints (Integrated with Ratu)

| Method | Endpoint | Purpose | Auth | Status |
|--------|----------|---------|------|--------|
| GET | `/` | Portal UI (Landing + Admin Panel) | No | Working |
| POST | `/api/auth/register` | Register user (proxied to identity) | No | Working |
| POST | `/api/auth/login` | Login & get JWT | No | Working |
| GET | `/api/auth/me` | Get current user (proxied to identity) | Yes Bearer | Working |
| GET | `/api/attendance/{event_id}` | Get event attendance from Ratu | Yes Bearer | Working |
| POST | `/api/checkins` | Create check-in on Ratu | Yes Bearer | Working |
| GET | `/api/checkins` | Get user check-ins (graceful fallback) | Yes Bearer | Working |

### Test TUGAS 3 Endpoints

#### Step 1: Get JWT Token
```bash
# Register
curl -X POST http://localhost:18081/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "petugas1",
    "password": "pass123",
    "role": "committee"
  }' | jq .

# Login
LOGIN=$(curl -s -X POST http://localhost:18081/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"petugas1","password":"pass123"}')
TOKEN=$(echo $LOGIN | jq -r '.access_token')
echo "Token: $TOKEN"
```

#### Step 2: Get Attendance Data from Ratu
```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:18081/api/attendance/E001 | jq .

# Expected Response:
# {
#   "event_id": "E001",
#   "total": 3,
#   "records": [
#     {
#       "event_id": "E001",
#       "ticket_id": "T001",
#       "checked_in_at_utc": "2026-01-08T...",
#       "checked_in_by": "admin"
#     }
#   ]
# }
```

#### Step 3: Create Check-in on Ratu
```bash
curl -X POST http://localhost:18081/api/checkins \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "E001",
    "ticket_id": "T999"
  }' | jq .

# Expected Response:
# {
#   "message": "check-in recorded",
#   "record": {
#     "event_id": "E001",
#     "ticket_id": "T999",
#     "checked_in_at_utc": "2026-01-08T...",
#     "checked_in_by": "petugas1"
#   }
# }
```

#### Step 4: Get User Check-ins
```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:18081/api/checkins" | jq .

# Expected Response (graceful fallback):
# {
#   "message": "Get user checkins not yet supported by Ratu API",
#   "user_id": "petugas1"
# }
```

### System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser["Browser<br/>https://dina.theokaitou.my.id"]
        Terminal["Terminal/curl<br/>API Testing"]
    end

    subgraph "External Services"
        Cloudflare["Cloudflare Tunnel<br/>Domain Routing"]
        Ratu["Ratu Attendance Service<br/>External Public API"]
    end

    subgraph "Dina Portal Services"
        Nginx["Nginx Reverse Proxy<br/>Port 18081"]
        Portal["Portal Service<br/>FastAPI Port 8000"]
        Identity["Identity Service<br/>FastAPI Port 8000"]
        DB["PostgreSQL<br/>Port 5432"]
    end

    Browser -->|HTTPS| Cloudflare
    Terminal -->|HTTPS| Cloudflare
    Cloudflare -->|Port 18081| Nginx
    Nginx -->|Internal| Portal
    Portal -->|JWT Auth| Identity
    Portal -->|HTTP/JWT| Ratu
    Identity -->|Query/Persist| DB
    Portal -->|Read Cache| DB
```

---

## Production Deployment on STB

### Access Information

#### Public URLs
```
Portal (DINA):           https://dina.theokaitou.my.id
Ratu Attendance:         https://ratu.theokaitou.my.id
```

#### SSH Access
```bash
# Connect via Cloudflare Tunnel
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id

# Services location on STB
cd /opt/tst-dina-identity-portal
```

#### Internal URLs (from STB)
```
Portal Service:          http://localhost:18081
Identity Service:        http://localhost:8000 (internal Docker)
Database:               postgresql://dina_user:password@db:5432/identity
```

### Deployment Steps

#### Prerequisites
- SSH access ke STB via Cloudflare
- Docker & Docker Compose installed
- Port 80/443 available (or reverse proxy configured)

#### 1. Clone Repository
```bash
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id

cd /opt
git clone https://github.com/Irdinailmunaa/tst-dina-identity-portal.git
cd tst-dina-identity-portal
```

#### 2. Configure Environment
```bash
# Copy production env template
cp .env .env.production

# Edit with production secrets
nano .env.production

# Required variables:
# JWT_SECRET=<generate-with-openssl-rand-hex-32>
# IDENTITY_BASE_URL=http://identity-service:8000 (internal)
# ATTENDANCE_BASE_URL=https://ratu.theokaitou.my.id (public)
# POSTGRES_USER=dina_user
# POSTGRES_PASSWORD=<secure-password>
```

#### 3. Build & Deploy
```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Verify
docker-compose -f docker-compose.prod.yml ps
```

#### 4. Test Deployment
```bash
# Health check
curl -s https://dina.theokaitou.my.id/health | jq .

# Test registration
curl -X POST https://dina.theokaitou.my.id/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test1","password":"test123","role":"admin"}' | jq .

# Test login
curl -X POST https://dina.theokaitou.my.id/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test1","password":"test123"}' | jq .
```

#### 5. Nginx Configuration
```bash
# Nginx should already be configured to:
# - Listen on port 80/443
# - Proxy requests to portal service on port 18081
# - Handle SSL/TLS via Cloudflare or local certs

# Current setup:
# - nginx-proxy-prod container listens on port 18081
# - Cloudflare tunnel routes dina.theokaitou.my.id → localhost:18081
```

### Service Status

```bash
# Check all containers
docker-compose -f docker-compose.prod.yml ps

# Expected output:
# NAME                    STATUS
# dina-db-prod           Up (healthy)
# identity-service-prod  Up
# portal-service-prod    Up
# nginx-proxy-prod       Up
```

### Monitoring & Logs

```bash
# View real-time logs
docker-compose -f docker-compose.prod.yml logs -f

# Specific service logs
docker-compose -f docker-compose.prod.yml logs -f portal-service-prod
docker-compose -f docker-compose.prod.yml logs -f identity-service-prod

# Check database health
docker-compose -f docker-compose.prod.yml logs -f dina-db-prod
```



## System Architecture Overview

### Components

```mermaid
graph TB
    subgraph "External"
        Users["External Users<br/>Browser/Mobile"]
        Ratu["Ratu System<br/>Attendance Mgmt"]
    end

    subgraph "Portal Service"
        Portal["Portal Service<br/>FastAPI<br/>GET / → UI<br/>POST /api/auth/* → Auth<br/>GET /api/attendance/* → Ratu<br/>POST/GET /api/checkins → Ratu"]
    end

    subgraph "Backend Services"
        Identity["Identity Service<br/>FastAPI<br/>JWT Auth<br/>User Management"]
        DB["PostgreSQL<br/>Data Persistence"]
    end

    Users -->|HTTPS| Portal
    Ratu -->|JWT API| Portal
    Portal -->|Internal| Identity
    Portal -->|Internal| DB
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Web Framework** | FastAPI | 0.115.0 | Async REST API |
| **Language** | Python | 3.11 | Core implementation |
| **Server** | Uvicorn | 0.30.6 | ASGI server |
| **Authentication** | PyJWT | 2.8.0 | JWT token handling |
| **Password Security** | Bcrypt | 4.1.1 | Password hashing |
| **HTTP Client** | httpx | 0.27.2 | Async Ratu API calls |
| **Database** | PostgreSQL | 15-alpine | Data persistence |
| **Container** | Docker | Latest | Deployment |
| **Orchestration** | Docker Compose | 3.8+ | Multi-container |

---

## Security Architecture

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Portal
    participant Identity
    participant Ratu

    User->>Portal: POST /api/auth/register
    Portal->>Identity: Create user (proxied)
    Identity->>Identity: Hash password (Bcrypt)
    Identity-->>Portal: User created
    Portal-->>User: Success

    User->>Portal: POST /api/auth/login
    Portal->>Identity: Authenticate
    Identity->>Identity: Verify password
    Identity-->>Portal: JWT token
    Portal-->>User: Token (HS256)

    User->>Portal: GET /api/attendance/{event_id}
    Portal->>Portal: Extract token
    Portal->>Portal: Verify JWT signature
    Portal->>Ratu: API call with JWT
    Ratu-->>Portal: Attendance data
    Portal-->>User: Data response
```

### Security Features

 JWT Authentication
- Algorithm: HS256
- Shared secret: `RatuDinaTST2026_`
- Expiry: 60 minutes
- Claims: sub (user_id), role, iat, exp

 Password Security
- Hashing: Bcrypt with salt rounds 12
- Never stored in plain text
- Comparison done securely

 API Security
- Bearer token in Authorization header
- Protected endpoints require valid JWT
- Token claims validated on each request
- Proper error handling (no info leakage)

 Data Security
- Database credentials in environment variables
- Secrets not committed to git
- HTTPS/TLS for all external communication
- Internal services on isolated Docker network

---

## Configuration Reference

### Development (.env)
```env
JWT_SECRET=RatuDinaTST2026_
JWT_ALG=HS256
TOKEN_EXPIRE_MINUTES=60
IDENTITY_BASE_URL=http://identity-service:8000
ATTENDANCE_BASE_URL=http://attendance_service:8000
```

### Production (.env.production)
```env
JWT_SECRET=<strong-random-secret-generated>
JWT_ALG=HS256
TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql://user:password@neon-provider/dina_prod
POSTGRES_USER=dina_user
POSTGRES_PASSWORD=<strong-password>
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.115.0 |
| **Language** | Python | 3.11 |
| **Server** | Uvicorn | 0.30.6 |
| **Authentication** | JWT (PyJWT) | 2.8.0 |
| **Password Hash** | Bcrypt | 4.1.1 |
| **Database** | PostgreSQL | 15-alpine |
| **Containerization** | Docker | Latest |
| **Composition** | Docker Compose | 3.8+ |

---

---

## Port Mapping

| Service | Development | Production | Type |
|---------|-------------|-----------|------|
| Identity Service | localhost:18080 | Internal only | Private API |
| Portal Service | localhost:18081 | https://dina.theokaitou.my.id:18081 | Public |
| PostgreSQL | localhost:5433 | Internal only | Database |

---

## Docker Commands

```bash
# Development - Start/Stop
docker-compose up -d --build        # Start all services
docker-compose down                 # Stop all services
docker-compose ps                   # List services & status
docker-compose logs -f              # View real-time logs
docker-compose logs identity-service --tail=50  # Last 50 lines

# Production
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml ps
```
---


## Security Features

 **Authentication & Authorization**
- JWT token-based authentication (HS256 algorithm)
- Bcrypt password hashing (salt rounds: 12)
- Bearer token in Authorization header
- 60-minute token expiry

 **Data Protection**
- Environment variables for secrets (not in git)
- PostgreSQL connection encrypted
- HTTPS support for production

 **API Security**
- Input validation (Pydantic)
- Protected endpoints requiring JWT
- Error handling without information leakage

---

## Key Concepts Implemented

### 1. JWT Authentication
- Stateless token-based auth
- No session storage required
- Claims: sub (username), role, iat (issued at), exp (expiry)
- Signature verification on each request

### 2. Microservices Architecture
- Identity service as independent component
- Can be consumed by multiple services
- Docker network for internal communication
- Scalable & cloud-ready

### 3. Best Practices
- REST API conventions
- Proper HTTP status codes
- Environment-based configuration
- Docker containerization
- Database persistence
- Health checks for monitoring

---

## Troubleshooting

### Service won't start
```bash
# Check logs
docker-compose logs identity-service

# Common issues:
# - Port already in use: lsof -i :18080
# - Database connection: Check DATABASE_URL in .env
# - JWT_SECRET not set: Verify .env file
```

### Token validation failing
```bash
# Verify token format
curl -X GET http://localhost:18080/auth/me \
  -H "Authorization: Bearer eyJ..." -v

# Check token expiry
echo "token" | cut -d. -f2 | base64 -d | jq .
```

### Database connection error
```bash
# Check database container
docker-compose ps dina-db

# Check database logs
docker-compose logs dina-db

# Test connection manually
psql -h localhost -p 5433 -U dina_user -d identity
```


