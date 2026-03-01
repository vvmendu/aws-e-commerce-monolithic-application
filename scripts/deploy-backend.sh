#!/bin/bash
# Run this on Backend EC2 instances after git clone
set -e

echo "=== Deploying Backend ==="
cd /home/ec2-user/backend

# Install Python dependencies
pip3 install -r requirements.txt

# Copy and fill in .env (update values before running)
if [ ! -f .env ]; then
  cp .env.example .env
  echo "⚠️  Please edit .env with your actual values before starting the service!"
  exit 1
fi

# Install systemd service
sudo tee /etc/systemd/system/ecommerce-backend.service > /dev/null <<EOF
[Unit]
Description=E-Commerce Backend API
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/backend
EnvironmentFile=/home/ec2-user/backend/.env
ExecStart=/usr/bin/python3 /home/ec2-user/backend/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ecommerce-backend
sudo systemctl start ecommerce-backend
sudo systemctl status ecommerce-backend

echo "=== Backend deployed successfully ==="
