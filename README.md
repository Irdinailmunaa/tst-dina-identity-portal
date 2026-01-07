# 🔐 DINA - TST Identity Service (Tugas 2) & Portal (Tugas 3)

**DINA** adalah sistem microservices untuk identity management dan operational check-in portal yang terintegrasi dengan Attendance Service (Ratu). Dikembangkan sebagai submission untuk **UAS II3160 Teknologi Sistem Terintegrasi**.

- **Tugas 2**: Core Identity Service (standalone JWT authentication) - **PRODUCTION READY**
- **Tugas 3**: Identity Portal + Integration dengan Ratu Attendance API (Admin/Committee panel)

---

## 📊 Struktur Project

```
tst-dina-identity-portal/
├── identity/service/        # ⭐ TUGAS 2: Identity Service (Core)
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
├── TUGAS_2.md              # ⭐ Tugas 2 Formal Document
├── MAKALAH.md              # Tugas 3 paper
├── ARCHITECTURE.md         # System design & flow
├── DEPLOYMENT.md           # Step-by-step deployment
├── docker-compose.yml      # Development setup
├── docker-compose.prod.yml # Production setup
└── README.md               # This file
```

---

## 🎯 TUGAS 2: Identity Service

### Quick Start

```bash
cd /Users/apple/Documents/tst-dina-identity-portal

# Start services (identity + portal + db)
docker-compose up -d --build

# Verify running
docker-compose ps

# Check health
curl http://localhost:18080/health
```

### Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/` | Welcome & endpoint list | ❌ |
| GET | `/health` | Health check | ❌ |
| POST | `/auth/register` | Register user | ❌ |
| POST | `/auth/login` | Login & get JWT | ❌ |
| GET | `/auth/me` | Get current user info | ✅ Bearer token |
| GET | `/docs` | Swagger UI | ❌ |

### API Examples (Curl Commands)

#### 1️⃣ Health Check
```bash
curl -s http://localhost:18080/health | jq .
# Response: {"status":"ok","service":"identity"}
```

#### 2️⃣ Register New User
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

#### 3️⃣ Login (Get JWT Token)
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

#### 4️⃣ Use Token to Get User Info (Protected Endpoint)
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
```

---

## � Production Deployment

### Prerequisites
- SSH access ke STB: `ssh -o ProxyCommand="cloudflared access ssh --hostname %h" root@ssh.theokaitou.my.id`
- Domain: https://dina.theokaitou.my.id:18080

### Deploy Steps
```bash
# 1. SSH ke STB
ssh -o ProxyCommand="cloudflared access ssh --hostname %h" root@ssh.theokaitou.my.id

# 2. Clone & setup
cd /opt
git clone https://github.com/Irdinailmunaa/tst-dina-identity-portal.git
cd tst-dina-identity-portal

# 3. Configure production env
cp .env.production .env
nano .env  # Set JWT_SECRET & DATABASE_URL

# 4. Deploy
docker-compose -f docker-compose.prod.yml up -d --build

# 5. Verify
curl https://dina.theokaitou.my.id:18080/health
```

---

## 📚 Documentation

- **[TUGAS_2.md](./TUGAS_2.md)** ⭐ - Formal document untuk submission (Abstrak, Spesifikasi, Implementasi, Testing)
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System design, security flow, integration diagram
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Detailed deployment guide
- **[MAKALAH.md](./MAKALAH.md)** - Tugas 3 paper template (akan ditulis lebih lanjut)

---

## 🔧 Configuration

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

## 📦 Technology Stack

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

## � Port Mapping

| Service | Development | Production | Type |
|---------|-------------|-----------|------|
| Identity Service | localhost:18080 | Internal only | Private API |
| Portal Service | localhost:18081 | https://dina.theokaitou.my.id:18081 | Public |
| PostgreSQL | localhost:5433 | Internal only | Database |

---

## �🐳 Docker Commands

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

## ✅ Deployment Checklist

- [ ] Verify local tests passing (curl commands above)
- [ ] Review TUGAS_2.md document
- [ ] SSH access ke STB working
- [ ] Clone repository ke /opt on STB
- [ ] Configure .env.production dengan secure secrets
- [ ] Generate strong JWT_SECRET: `openssl rand -hex 32`
- [ ] Build images: `docker-compose -f docker-compose.prod.yml build`
- [ ] Start services: `docker-compose -f docker-compose.prod.yml up -d`
- [ ] Test health endpoint: `curl https://dina.theokaitou.my.id:18080/health`
- [ ] Test register/login endpoints
- [ ] Check logs untuk errors
- [ ] Monitor service health

---

## � Security Features

✅ **Authentication & Authorization**
- JWT token-based authentication (HS256 algorithm)
- Bcrypt password hashing (salt rounds: 12)
- Bearer token in Authorization header
- 60-minute token expiry

✅ **Data Protection**
- Environment variables for secrets (not in git)
- PostgreSQL connection encrypted
- HTTPS support for production

✅ **API Security**
- Input validation (Pydantic)
- Protected endpoints requiring JWT
- Error handling without information leakage

---

## 🎓 Key Concepts Implemented

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

## 📞 Troubleshooting

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

---

## 📝 Submission Requirements

### Tugas 2 Submission
- ✅ **GitHub Repository**: https://github.com/Irdinailmunaa/tst-dina-identity-portal
- ✅ **Formal Document**: [TUGAS_2.md](./TUGAS_2.md)
- ✅ **Source Code**: Complete implementation in `identity/service/`
- ✅ **Docker Setup**: Working docker-compose.yml & docker-compose.prod.yml
- ✅ **Testing**: Curl examples & verified endpoints
- ✅ **Deployment**: Production-ready on STB

### Tugas 3 Submission (Next)
- ⏳ **Portal Implementation**: Admin/inspector panel
- ⏳ **Ratu Integration**: API integration for attendance
- ⏳ **Makalah**: Full technical paper in MAKALAH.md
- ⏳ **Deployment**: Portal on https://dina.theokaitou.my.id:18081

---

## 🤝 Integration dengan Ratu Service

**Koordinasi Tugas 3:**
1. Dapatkan Ratu API endpoint URL (public)
2. Tanya authentication method:
   - Shared JWT_SECRET untuk kedua service?
   - Atau API key terpisah?
3. Request test endpoint untuk development
4. Confirm request/response format:
   - POST /checkins: `{"user_id": "...", "event_id": "...", ...}`
   - GET /attendance/{event_id}: Response structure
5. Update portal integration code

---

## 📚 Resources & References

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **JWT.io**: https://jwt.io/
- **Bcrypt**: https://github.com/pyca/bcrypt
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **REST API Design**: https://restfulapi.net/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Reference Project**: Healthy Grocery Recommendation API (Favian & Ahmad)

---

## 📄 Files Overview

| File | Purpose |
|------|---------|
| **TUGAS_2.md** | ⭐ Formal Tugas 2 document (submit this) |
| **README.md** | Project overview & quick start |
| **ARCHITECTURE.md** | System design & diagrams |
| **DEPLOYMENT.md** | Step-by-step deployment guide |
| **docker-compose.yml** | Development configuration |
| **docker-compose.prod.yml** | Production configuration |
| **.env** | Development secrets (git-ignored) |
| **.env.production** | Production template |

---

## ✨ Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Identity Service | ✅ Production Ready | All endpoints tested |
| Docker Setup | ✅ Complete | Dev & prod compose files |
| Documentation | ✅ Complete | TUGAS_2.md + guides |
| Testing | ✅ Manual tested | Curl examples provided |
| Deployment | ✅ Ready | Can deploy to STB |
| Portal (Tugas 3) | ⏳ In Progress | UI ready, awaiting Ratu API |
| Ratu Integration | ⏳ Blocked | Waiting for Ratu endpoints |

---

**Created**: January 7, 2026  
**Last Updated**: January 7, 2026  
**Status**: Tugas 2 - Production Ready | Tugas 3 - In Development  
**Maintainer**: Irdinah Ilmunaa

---

## 🎯 Next Steps

1. **Test locally** - Run curl commands above ✅
2. **Review TUGAS_2.md** - Ensure all requirements met ✅
3. **Deploy to STB** - Follow DEPLOYMENT.md
4. **Get Ratu API info** - Coordinate with Ratu team
5. **Complete Tugas 3** - Portal + integration
6. **Write makalah** - Full technical paper
7. **Submit** - GitHub links + documentation
