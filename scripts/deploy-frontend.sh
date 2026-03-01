#!/bin/bash
# Run this on Frontend EC2 instances after git clone
set -e

echo "=== Deploying Frontend ==="
cd /home/ec2-user/frontend

# Install Node.js dependencies
npm install --production

# Copy and fill in .env (update values before running)
if [ ! -f .env ]; then
  cp .env.example .env
  echo "⚠️  Please edit .env with your actual values before starting the service!"
  exit 1
fi

# Install systemd service
sudo tee /etc/systemd/system/ecommerce-frontend.service > /dev/null <<EOF
[Unit]
Description=E-Commerce Frontend
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/frontend
EnvironmentFile=/home/ec2-user/frontend/.env
ExecStart=/usr/bin/node /home/ec2-user/frontend/server.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ecommerce-frontend
sudo systemctl start ecommerce-frontend
sudo systemctl status ecommerce-frontend

echo "=== Frontend deployed successfully ==="
