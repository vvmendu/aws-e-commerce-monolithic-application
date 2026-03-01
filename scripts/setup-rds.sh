#!/bin/bash
# Run from a backend EC2 instance to initialize the RDS database
# Usage: RDS_ENDPOINT=your-rds-endpoint.rds.amazonaws.com DB_PASSWORD=yourpassword bash setup-rds.sh

RDS_ENDPOINT=${RDS_ENDPOINT:-"your-rds-endpoint.rds.amazonaws.com"}
DB_USER=${DB_USER:-"admin"}
DB_PASSWORD=${DB_PASSWORD:-""}
DB_NAME="ecommerce_db"

echo "=== Initializing RDS Database ==="
mysql -h $RDS_ENDPOINT -u $DB_USER -p$DB_PASSWORD < /home/ec2-user/database/schema.sql
echo "Schema loaded."
mysql -h $RDS_ENDPOINT -u $DB_USER -p$DB_PASSWORD $DB_NAME < /home/ec2-user/database/seed-data.sql
echo "Seed data loaded."
mysql -h $RDS_ENDPOINT -u $DB_USER -p$DB_PASSWORD -e "SELECT COUNT(*) AS total_products FROM products;" $DB_NAME
echo "=== RDS setup complete ==="
