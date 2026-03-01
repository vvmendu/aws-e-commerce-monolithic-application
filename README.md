# ShopNow - AWS E-Commerce Monolith

Full-stack e-commerce platform on AWS (Node.js Frontend + Python Flask Backend + MySQL RDS).

## Repo Structure
```
├── backend/          # Python Flask API
├── frontend/         # Node.js Express frontend
├── database/         # MySQL schema and seed data
└── scripts/          # Deployment scripts
```

## Quick Start (on EC2)

### 1. Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git /home/ec2-user/
```

### 2. Backend EC2
```bash
cd /home/ec2-user/backend
cp .env.example .env
nano .env   # fill in DB_HOST, DB_PASSWORD, JWT_SECRET_KEY
bash /home/ec2-user/scripts/deploy-backend.sh
```

### 3. Frontend EC2
```bash
cd /home/ec2-user/frontend
cp .env.example .env
nano .env   # fill in API_BASE_URL pointing to backend private IP
bash /home/ec2-user/scripts/deploy-frontend.sh
```

### 4. Initialize RDS (run from backend EC2)
```bash
sudo yum install mysql -y
RDS_ENDPOINT=your-endpoint.rds.amazonaws.com DB_PASSWORD=yourpass bash /home/ec2-user/scripts/setup-rds.sh
```

## Default Credentials
- Admin: admin@shopnow.com / Admin@12345
- Test User: alice@example.com / Test@12345
