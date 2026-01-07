#!/bin/bash

# Deployment script to update STB with nginx HTTPS proxy

echo "Step 1: Create tarball with new docker-compose and nginx config..."
tar -czf /tmp/tixgo_nginx_deploy.tar.gz \
  docker-compose.prod.yml \
  nginx-prod.conf \
  ssl/nginx.crt \
  ssl/nginx.key

echo "Step 2: Copy tarball to STB via cloudflared..."
scp -o ProxyCommand='cloudflared access ssh --hostname %h' \
  /tmp/tixgo_nginx_deploy.tar.gz \
  root@ssh.theokaitou.my.id:/opt/tmp_nginx_deploy.tar.gz

echo "Step 3: Extract and update files on STB..."
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id << 'REMOTE_COMMANDS'
cd /opt/tst-dina-identity-portal
tar -xzf /opt/tmp_nginx_deploy.tar.gz
echo "Files extracted"
REMOTE_COMMANDS

echo "Step 4: Rebuild and restart docker-compose on STB..."
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id << 'REMOTE_COMMANDS'
cd /opt/tst-dina-identity-portal
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
echo "Containers rebuilt and started"
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'prod|nginx'
REMOTE_COMMANDS

echo "Step 5: Update cloudflared config to use HTTPS..."
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id << 'REMOTE_COMMANDS'
# Create updated cloudflared config
cp /root/.cloudflared/config.yml /root/.cloudflared/config.yml.backup

cat > /root/.cloudflared/config.yml << 'CLOUDFLARED_CONFIG'
tunnel: c0b86801-c8ab-493d-af0d-550d21b058bf
credentials-file: /root/.cloudflared/c0b86801-c8ab-493d-af0d-550d21b058bf.json

ingress:
  - hostname: losiento.my.id
    service: http://localhost:8765
  - hostname: dina.theokaitou.my.id
    service: https://localhost:18081
    originRequest:
      disableTlsVerification: true
  - service: http_status:404
CLOUDFLARED_CONFIG

systemctl restart cloudflared
sleep 2
systemctl status cloudflared --no-pager | head -10
REMOTE_COMMANDS

echo "✅ Deployment complete!"
echo "Test: curl -k https://dina.theokaitou.my.id/"
