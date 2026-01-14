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

# Create default dev user from environment variables
echo "Setting up Airflow user..."
AIRFLOW_USERNAME=${AIRFLOW_USERNAME:-dev_user}
AIRFLOW_PASSWORD=${AIRFLOW_PASSWORD:-dev_user}
AIRFLOW_EMAIL=${AIRFLOW_EMAIL:-dev@example.com}

airflow users create \
    --username "$AIRFLOW_USERNAME" \
    --firstname Airflow \
    --lastname User \
    --role Admin \
    --email "$AIRFLOW_EMAIL" \
    --password "$AIRFLOW_PASSWORD" || echo "User already exists"

echo "Airflow user setup complete. Username: $AIRFLOW_USERNAME"

echo "Starting Airflow webserver and scheduler..."
# Start scheduler in background
airflow scheduler &
SCHEDULER_PID=$!

# Start webserver in foreground
exec airflow webserver --port 8080