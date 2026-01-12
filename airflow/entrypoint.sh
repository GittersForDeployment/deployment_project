#!/bin/bash
set -e

# Wait for MySQL to be ready
echo "Waiting for MySQL at $MYSQL_HOST:$MYSQL_PORT..."
while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 1
done
echo "MySQL is ready"

# Initialize Airflow database
echo "Initializing Airflow database..."
airflow db migrate

# Create default admin user
echo "Setting up admin user..."
if airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin 2>/dev/null; then
  echo "Admin user created"
else
  echo "Admin user already exists"
fi

echo "Starting Airflow..."
exec airflow standalone