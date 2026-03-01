# aws-e-commerce-monolithic-application
AWS E-Commerce Monolithic Application
=============================================================================================
ecommerce-aws/
├── README.md
├── backend/
│   ├── app.py              ← Flask app factory
│   ├── config.py           ← DB/JWT/S3 config
│   ├── requirements.txt    ← Python deps
│   ├── .env.example        ← Template for secrets
│   ├── models/             ← user, product, cart, order
│   ├── routes/             ← auth, products, cart, orders, categories
│   └── middleware/         ← JWT auth, error handler
├── frontend/
│   ├── server.js           ← Express app
│   ├── package.json
│   ├── .env.example
│   ├── routes/             ← index, products, cart, auth
│   ├── views/              ← EJS templates (index, products, cart, login, etc.)
│   └── public/             ← style.css, cart.js
├── database/
│   ├── schema.sql          ← All tables (users, products, orders, etc.)
│   └── seed-data.sql       ← Categories + sample products
└── scripts/
    ├── deploy-backend.sh   ← Installs deps + systemd service
    ├── deploy-frontend.sh  ← Installs deps + systemd service
    └── setup-rds.sh        ← Loads schema + seed into RDS

=============================================================================================
BACKEND EC2 ( Both 1a and 1B)
====================================================
# Install deps (user data already handles this on launch)
sudo yum install python3 python3-pip git mysql -y

# Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git /home/ec2-user/app
cd /home/ec2-user/app/backend

# Configure secrets
cp .env.example .env
nano .env   # Set DB_HOST, DB_PASSWORD, JWT_SECRET_KEY

# Deploy as a service
bash /home/ec2-user/app/scripts/deploy-backend.sh

=============================================================================================
FRONTEND EC2 ( Both 1a and 1B)
====================================================
sudo yum install nodejs git -y

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git /home/ec2-user/app
cd /home/ec2-user/app/frontend

cp .env.example .env
nano .env   # Set API_BASE_URL to backend private IP

bash /home/ec2-user/app/scripts/deploy-frontend.sh

=============================================================================================
Initialize RDS ( RUN From Any Backend EC2 )
=================================================

RDS_ENDPOINT=your-endpoint.rds.amazonaws.com \
DB_PASSWORD=yourpassword \
bash /home/ec2-user/app/scripts/setup-rds.sh

=============================================================================================

