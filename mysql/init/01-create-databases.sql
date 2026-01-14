CREATE DATABASE IF NOT EXISTS airflow_metadata;
CREATE DATABASE IF NOT EXISTS pipeline_data;

GRANT ALL PRIVILEGES ON airflow_metadata.* TO 'airflow_user'@'%';
GRANT ALL PRIVILEGES ON pipeline_data.* TO 'airflow_user'@'%';
FLUSH PRIVILEGES;