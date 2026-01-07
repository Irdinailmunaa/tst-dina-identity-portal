#!/bin/bash
set -e

HOST="root@ssh.theokaitou.my.id"
PROXY="-o ProxyCommand='cloudflared access ssh --hostname %h'"

echo "Copying files to STB..."
scp $PROXY docker-compose.prod.yml "$HOST:/opt/tst-dina-identity-portal/"
scp $PROXY nginx-prod.conf "$HOST:/opt/tst-dina-identity-portal/"

echo "Deploying on STB..."
ssh $PROXY -t "$HOST" "cd /opt/tst-dina-identity-portal && docker-compose -f docker-compose.prod.yml down && sleep 3 && docker-compose -f docker-compose.prod.yml up -d && sleep 5 && docker-compose -f docker-compose.prod.yml ps"

echo "Testing endpoint..."
curl -k https://dina.theokaitou.my.id/ 2>&1 | head -30

echo "✅ Done!"
