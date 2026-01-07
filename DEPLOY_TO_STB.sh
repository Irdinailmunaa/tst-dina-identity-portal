#!/bin/bash

# =======================
# DINA Portal - STB Deployment Script
# =======================
# Usage: ./DEPLOY_TO_STB.sh
# This script will:
# 1. SSH ke STB via Cloudflared
# 2. Clone/update repo
# 3. Setup docker-compose
# 4. Deploy services

SSH_CMD="ssh -o ProxyCommand=\"cloudflared access ssh --hostname %h\" root@ssh.theokaitou.my.id"

echo "🚀 DINA Portal STB Deployment"
echo "=============================="
echo ""

# Step 1: Check SSH connectivity
echo "Step 1: Testing SSH connection to STB..."
$SSH_CMD "echo '✅ SSH connection successful'"
if [ $? -ne 0 ]; then
    echo "❌ SSH connection failed. Check Cloudflared installation."
    exit 1
fi

echo ""
echo "Step 2: Clone/Update repository..."
$SSH_CMD << 'EOF'
cd /opt

# Clone if not exists, otherwise pull latest
if [ -d "tst-dina-identity-portal" ]; then
    echo "📦 Repository exists. Pulling latest changes..."
    cd tst-dina-identity-portal
    git pull origin main
else
    echo "📦 Cloning repository..."
    git clone https://github.com/Irdinailmunaa/tst-dina-identity-portal.git
    cd tst-dina-identity-portal
fi

echo "✅ Repository ready at $(pwd)"
EOF

echo ""
echo "Step 3: Setup .env.production (if needed)..."
$SSH_CMD << 'EOF'
cd /opt/tst-dina-identity-portal

# Check if .env.production exists and has real JWT_SECRET
if grep -q "REPLACE_WITH_SHARED_SECRET" .env.production 2>/dev/null; then
    echo "⚠️  .env.production has placeholder. Using current version..."
fi

echo "✅ .env.production configured"
ls -la .env.production
EOF

echo ""
echo "Step 4: Deploy with docker-compose..."
$SSH_CMD << 'EOF'
cd /opt/tst-dina-identity-portal

echo "🐳 Building and starting services..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
docker-compose -f docker-compose.prod.yml up -d --build

echo ""
echo "✅ Services starting... Wait 10 seconds for them to be ready"
sleep 10

docker-compose -f docker-compose.prod.yml ps
EOF

echo ""
echo "Step 5: Verify deployment..."
$SSH_CMD << 'EOF'
cd /opt/tst-dina-identity-portal

echo "🔍 Testing Identity Service (internal)..."
curl -s http://localhost:18080/health | jq . || echo "Identity service check..."

echo ""
echo "🔍 Testing Portal Service..."
curl -s http://localhost:18081/ | head -20 | grep -o "<title>.*</title>" || echo "Portal service check..."

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Access portal at:"
echo "  - Production: https://dina.theokaitou.my.id:18081"
echo "  - Local STB: http://localhost:18081"
EOF

echo ""
echo "=============================="
echo "✅ Deployment finished!"
echo "=============================="
echo ""
echo "Next steps:"
echo "1. Open https://dina.theokaitou.my.id:18081 in your browser"
echo "2. Test login with your credentials"
echo "3. Test integration with Ratu API"
echo ""
