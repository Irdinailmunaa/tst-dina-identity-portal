# TST DINA Identity Portal - Deployment Guide

## 📋 Overview
Sistem identity dan portal untuk TST (Tix Student Trackings) dengan:
- **Identity Service**: Authentication & Authorization (Port 18080 - Internal)
- **Portal Service**: Public Web Portal (Port 18081 - Public)
- **PostgreSQL**: Database (Port 5433 - Internal)

---

## 🚀 Quick Start (Development)

### Prerequisites
- Docker & Docker Compose
- macOS/Linux/Windows

### Start Services
```bash
cd /Users/apple/Documents/tst-dina-identity-portal

# Development mode
docker-compose up -d --build

# Check status
docker-compose ps
```

### Test Services
```bash
# Identity Service Health
curl http://localhost:18080/health

# Portal Service Health
curl http://localhost:18081/health

# API Documentation
open http://localhost:18080/docs
```

---

## 🌍 Production Deployment (STB)

### Prerequisites on STB Server
```bash
# Install Docker & Docker Compose
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker-compose --version
```

### SSH Access to STB
```bash
ssh -o ProxyCommand="cloudflared access ssh --hostname %h" root@ssh.theokaitou.my.id
```

### Clone Repository
```bash
cd /opt
git clone <repo-url> tst-dina-identity-portal
cd tst-dina-identity-portal
```

### Configure Production Environment
```bash
# Copy and edit production environment
cp .env.example .env.production

# Edit with secure values
nano .env.production
# Update:
# - JWT_SECRET (strong random key)
# - POSTGRES_PASSWORD (strong password)
# - Other sensitive data
```

### Deploy to Production
```bash
# Make deploy script executable
chmod +x deploy.sh

# Deploy using production compose file
docker-compose -f docker-compose.prod.yml down || true
docker-compose -f docker-compose.prod.yml up -d --build

# Verify deployment
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Access Production Services
```bash
# Public URL (via Cloudflare tunnel / reverse proxy)
https://dina.theokaitou.my.id:18081

# Health Check
curl https://dina.theokaitou.my.id:18081/health

# API Docs
https://dina.theokaitou.my.id:18081/docs
```

---

## 📝 Environment Variables

### Development (.env)
```
JWT_SECRET=RatuDinaTST2026_
JWT_ALG=HS256
TOKEN_EXPIRE_MINUTES=60
IDENTITY_BASE_URL=http://identity-service:8000
ATTENDANCE_BASE_URL=http://attendance_service:8000
```

### Production (.env.production)
```
JWT_SECRET=<strong-random-key>
POSTGRES_PASSWORD=<strong-password>
POSTGRES_USER=dina_user
POSTGRES_DB=identity_production
```

---

## 🔧 Management Commands

### Development
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f <service-name>

# Rebuild images
docker-compose up -d --build

# Remove everything
docker-compose down -v
```

### Production
```bash
# Start services
docker-compose -f docker-compose.prod.yml up -d --build

# Stop services
docker-compose -f docker-compose.prod.yml down

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Update & redeploy
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## 🔐 Security Notes

### Before Production Deployment
- [ ] Change JWT_SECRET to a strong random value
- [ ] Change database password to a strong value
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Enable database backups
- [ ] Set up monitoring & logging

### Database Backup
```bash
# Backup database
docker exec dina-db-prod pg_dump -U dina_user identity_production > backup.sql

# Restore database
docker exec -i dina-db-prod psql -U dina_user identity_production < backup.sql
```

---

## 📊 API Endpoints

### Identity Service (18080)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root - API Info |
| GET | `/health` | Health Check |
| POST | `/auth/register` | Register User |
| POST | `/auth/login` | Login User |
| GET | `/auth/me` | Get Current User |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc |

### Portal Service (18081)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health Check |
| GET | `/` | Home Page |
| POST | `/api/auth/register` | Proxy Register |
| POST | `/api/auth/login` | Proxy Login |
| GET | `/api/auth/me` | Proxy Get User |
| POST | `/api/checkins` | Proxy Checkins |
| GET | `/api/attendance/{event_id}` | Proxy Attendance |

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :18081

# Kill process
kill -9 <PID>
```

### Database Connection Error
```bash
# Check database is running
docker ps | grep dina-db

# Check database logs
docker logs dina-db-prod

# Verify connection
docker exec dina-db-prod psql -U dina_user -d identity_production -c "SELECT 1"
```

### Service Crashes
```bash
# Check logs
docker-compose logs <service-name>

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

---

## 📞 Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Review configuration: `.env` and `docker-compose.yml`
3. Verify network: `docker network inspect dina-net`

---

## 📅 Version History
- **v1.0.0** (2026-01-07): Initial release
