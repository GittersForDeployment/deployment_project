# Data Pipeline Deployment Project

## 📋 Project Overview

This project demonstrates a complete DevOps lifecycle for a microservices-based data pipeline application, from development to production deployment using Docker, Kubernetes, and CI/CD pipelines.

### 🎯 Project Objectives

Deploy a data engineering pipeline with:
- **Apache Airflow** for workflow orchestration
- **MySQL** database for data persistence
- **MySQL Workbench** for database monitoring
- Separate **Development** and **Production** environments
- Complete CI/CD automation
- Container-based microservices architecture

---

## 🏗️ Architecture Components

### Core Services

1. **MySQL Database** (2 instances)
   - `mysql-dev`: Development database
     - Database: `airflow_metadata` (Airflow's internal data)
     - Database: `pipeline_data` (Our ETL pipeline data)
   - `mysql-prod`: Production database
     - Database: `airflow_metadata` (Airflow's internal data)
     - Database: `pipeline_data` (Our ETL pipeline data)
   - Persistent storage with volumes
   - Secret management for credentials

2. **Apache Airflow** (2 instances)
   - `airflow-dev`: Development environment
   - `airflow-prod`: Production environment
   - Components per instance:
     - Webserver (UI for monitoring)
     - Scheduler
     - Worker(s)
     - Uses MySQL for metadata (same MySQL instance, different database)

3. **MySQL Workbench** (2 instances)
   - `workbench-dev`: Monitor development database
   - `workbench-prod`: Monitor production database
   - Web-based GUI for database management
   - **Primary use:** Query and monitor `pipeline_data` database
   - **Can also access:** `airflow_metadata` if needed (but Airflow UI is better for that)

### Data Pipeline Jobs

Each Airflow instance will run **3 DAGs** (Directed Acyclic Graphs):

1. **Data Simulation Job** (`dag_data_simulator.py`)
   - Generate synthetic data
   - Simulate real-world data sources
   - Insert raw data into MySQL

2. **Data Cleaning & Export Job** (`dag_data_cleaning.py`)
   - Clean and validate raw data
   - Transform data formats
   - Daily export functionality
   - Archive processed data

3. **Analytics & Aggregation Job** (`dag_analytics.py`)
   - Perform data aggregations
   - Generate analytics reports
   - Create summary tables
   - Calculate KPIs and metrics

---

## 📁 Project Structure

```
deployment_project/
├── README.md
├── .gitignore
├── .dockerignore
│
├── .env.example                  # Template for environment variables (committed)
├── .env.dev                      # Development secrets (gitignored)
├── .env.prod                     # Production secrets (gitignored)
│
├── airflow/                      # Airflow source code
│   ├── dags/                     # DAG definitions
│   │   ├── dag_data_simulator.py
│   │   ├── dag_data_cleaning.py
│   │   └── dag_analytics.py
│   ├── plugins/                  # Custom Airflow plugins
│   ├── config/                   # Airflow configuration
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Airflow container image
│
├── mysql/                        # MySQL configurations
│   ├── init/                     # Initialization scripts
│   │   ├── create_tables.sql
│   │   └── insert.sql
│   └── conf/                     # MySQL configuration files
│
├── docker-compose.dev.yml        # Development environment
├── docker-compose.prod.yml       # Production environment
│
├── deploy/                       # Kubernetes manifests
│   ├── namespaces/
│   ├── mysql/
│   │   ├── statefulset.yaml
│   │   ├── service.yaml
│   │   ├── pv.yaml
│   │   ├── pvc.yaml
│   │   ├── secrets.yaml          # Real secrets (gitignored)
│   │   └── secrets.example.yaml  # Template (committed)
│   ├── airflow/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   ├── secrets.yaml          # Real secrets (gitignored)
│   │   └── secrets.example.yaml  # Template (committed)
│   └── workbench/
│       ├── deployment.yaml
│       └── service.yaml
│
├── .github/workflows/            # CI/CD pipelines
│   ├── dev-pipeline.yml
│   └── prod-pipeline.yml
│
└── docs/                         # Additional documentation
    ├── architecture.md
    └── deployment-guide.md
```

---