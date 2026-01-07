# 🔐 TST DINA Identity Portal

A microservices-based identity and access management system for TST (Tix Student Trackings).

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Public Internet (HTTPS)                   │
│              https://dina.theokaitou.my.id:18081             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                ┌──────────▼──────────┐
                │  Portal Service     │
                │  (Port 18081)       │
                │  - Web UI           │
                │  - API Proxy        │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐    ┌────────▼────────┐   ┌────▼────┐
   │ Identity │    │   PostgreSQL    │   │ External│
   │ Service  │    │   Database      │   │ Services│
   │(18080)   │    │   (5433)        │   │(Ratu)   │
   └──────────┘    └─────────────────┘   └─────────┘
```

## 🚀 Quick Start

### Development
```bash
# Clone repository
git clone <repo-url>
cd tst-dina-identity-portal

# Start services
docker-compose up -d --build

# Test services
curl http://localhost:18080/health
curl http://localhost:18081/health

# View API docs
open http://localhost:18080/docs
```

### Production
```bash
# Deploy to STB server
ssh -o ProxyCommand="cloudflared access ssh --hostname %h" root@ssh.theokaitou.my.id

# Clone and deploy
cd /opt
git clone <repo-url> tst-dina-identity-portal
cd tst-dina-identity-portal
chmod +x deploy.sh
./deploy.sh

# Or manually
docker-compose -f docker-compose.prod.yml up -d --build
```

## 📋 Services

### Identity Service (Port 18080)
- JWT-based authentication
- User registration & login
- Token validation
- Role-based access control

**API Endpoints:**
```bash
GET  /health              # Health check
GET  /docs                # Swagger UI
POST /auth/register       # Register user
POST /auth/login          # Login & get token
GET  /auth/me             # Get current user
```

### Portal Service (Port 18081)
- Public web interface
- API proxy/gateway
- Static assets serving
- Integration with identity & attendance services

**Features:**
- Register & login users
- View attendance data
- Check-in management
- Responsive web UI

## 🔧 Configuration

### Environment Variables
Create `.env` file (development) or `.env.production` (production):

```env
# JWT Configuration
JWT_SECRET=your-secret-key
JWT_ALG=HS256
TOKEN_EXPIRE_MINUTES=60

# Service URLs
IDENTITY_BASE_URL=http://identity-service:8000
ATTENDANCE_BASE_URL=http://attendance_service:8000

# Database
DATABASE_URL=postgresql://user:password@db:5432/identity
POSTGRES_USER=user
POSTGRES_PASSWORD=password
```

## 📊 Port Mapping

| Service | Development | Production | Type |
|---------|-------------|-----------|------|
| Identity Service | localhost:18080 | Internal | Private API |
| Portal Service | localhost:18081 | https://dina.theokaitou.my.id:18081 | Public |
| PostgreSQL | localhost:5433 | Internal | Database |

## 🐳 Docker Commands

```bash
# Development
docker-compose up -d --build        # Start all services
docker-compose down                 # Stop all services
docker-compose logs -f              # View logs
docker-compose ps                   # List services

# Production
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml logs -f
```

## 📖 Documentation

- [Deployment Guide](./DEPLOYMENT.md) - Detailed deployment instructions
- [Setup Guide](./SETUP_GUIDE.md) - Initial setup information
- [API Documentation](http://localhost:18080/docs) - Interactive API docs (when running)

## 🔐 Security

- JWT tokens for authentication
- Bcrypt password hashing
- Environment variable management
- Database password protection
- HTTPS support for production

## 📦 Technology Stack

- **Framework**: FastAPI (Python)
- **Server**: Uvicorn
- **Database**: PostgreSQL
- **Authentication**: JWT + Bcrypt
- **Containerization**: Docker & Docker Compose
- **HTTP Client**: HTTPX

## 🤝 Integration Points

- **Attendance Service (Ratu)**: Event data & check-in management
- **Cloudflare Access**: Secure SSH tunnel to production server
- **PostgreSQL**: User data & session storage

## 📝 License

TST DINA Identity Portal - Internal Use

## 👥 Author

Created: January 7, 2026
