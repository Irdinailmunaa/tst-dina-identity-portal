#!/bin/bash
# Test & Integration Commands for DINA Tugas 3

# ============================================
# 1. LOCAL TESTING (Development)
# ============================================

echo "=== Test 1: Health Check ==="
curl -s http://localhost:18081/ | head -5

echo ""
echo "=== Test 2: Register New User ==="
curl -s -X POST http://localhost:18081/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123",
    "role": "admin"
  }' | jq .

echo ""
echo "=== Test 3: Login User ==="
TOKEN=$(curl -s -X POST http://localhost:18081/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"

echo ""
echo "=== Test 4: Validate Token ==="
curl -s -X GET http://localhost:18081/api/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq .

# ============================================
# 2. PRODUCTION TESTING (Once Deployed)
# ============================================

echo ""
echo "=== Production Tests (After Deployment) ==="
echo "Run these commands after deploying to STB:"
echo ""

echo "# Test 1: Access Portal"
echo "curl https://dina.theokaitou.my.id:18081/"
echo ""

echo "# Test 2: Login to Production"
echo "curl -X POST https://dina.theokaitou.my.id:18081/api/auth/login \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"username\": \"testuser\", \"password\": \"password123\"}' | jq ."
echo ""

echo "# Test 3: Call RATU API from DINA"
echo "curl -X POST https://dina.theokaitou.my.id:18081/api/checkins \\"
echo "  -H 'Authorization: Bearer \$TOKEN' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"event_id\": \"E001\", \"ticket_id\": \"T001\"}' | jq ."
echo ""

echo "# Test 4: Get Attendance Recap"
echo "curl -X GET https://dina.theokaitou.my.id:18081/api/attendance/E001 \\"
echo "  -H 'Authorization: Bearer \$TOKEN' | jq ."
echo ""

# ============================================
# 3. CROSS-DOMAIN TESTING
# ============================================

echo ""
echo "=== Cross-Domain JWT Validation Test ==="
echo ""
echo "This tests that token from DINA is valid in RATU:"
echo ""
echo "# 1. Get token from DINA"
echo "TOKEN=\$(curl -s -X POST https://dina.theokaitou.my.id:18081/api/auth/login \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"username\": \"testuser\", \"password\": \"password123\"}' | jq -r '.access_token')"
echo ""
echo "# 2. Use DINA token in RATU API call"
echo "curl -X POST https://ratu.theokaitou.my.id/api/checkins \\"
echo "  -H \"Authorization: Bearer \$TOKEN\" \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"event_id\": \"E001\", \"ticket_id\": \"T001\"}'"
echo ""
echo "Expected: Success (200) if JWT_SECRET is same"
echo "Expected: 401 Unauthorized if JWT_SECRET is different"
echo ""

# ============================================
# 4. DOCKER COMMANDS
# ============================================

echo ""
echo "=== Docker Useful Commands ==="
echo ""
echo "# Check services status"
echo "docker-compose ps"
echo ""
echo "# View logs"
echo "docker-compose logs -f portal-service"
echo "docker-compose logs -f identity-service"
echo ""
echo "# Restart services"
echo "docker-compose restart portal-service"
echo ""
echo "# Full rebuild"
echo "docker-compose down && docker-compose up -d --build"
echo ""

# ============================================
# 5. SSH TO STB
# ============================================

echo ""
echo "=== SSH to STB (Production Server) ==="
echo ""
echo "ssh -o ProxyCommand=\"cloudflared access ssh --hostname %h\" root@ssh.theokaitou.my.id"
echo ""
echo "After SSH:"
echo "cd /opt/tst-dina-identity-portal"
echo "docker-compose -f docker-compose.prod.yml ps"
echo "docker-compose -f docker-compose.prod.yml logs -f portal-service"
echo ""
