#!/bin/bash

# Create directory structure for identity service
mkdir -p identity/service/app
mkdir -p identity/service/static
mkdir -p identity/service/templates

# Create identity service files
touch identity/service/app/__init__.py
touch identity/service/app/auth.py
touch identity/service/app/security.py
touch identity/service/app/main.py
touch identity/service/Dockerfile
touch identity/service/requirements.txt

# Create directory structure for portal service
mkdir -p portal/service/app
mkdir -p portal/service/static
mkdir -p portal/service/templates

# Create portal service files
touch portal/service/app/__init__.py
touch portal/service/app/proxy.py
touch portal/service/app/main.py
touch portal/service/templates/index.html
touch portal/service/static/app.js
touch portal/service/static/styles.css
touch portal/service/Dockerfile
touch portal/service/requirements.txt

# Create root level files
touch docker-compose.yml
touch docker-compose.prod.yml
touch deploy.sh
touch .env.example
touch README.md

# Make deploy.sh executable
chmod +x deploy.sh

echo "✅ Project structure created successfully!"
