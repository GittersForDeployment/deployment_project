from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mysql.connector
import os

default_args = {
    'owner': 'nasai',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def get_mysql_connection():
    """Create MySQL connection"""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'mysql-dev'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'airflow_user'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('PIPELINE_DATABASE', 'pipeline_data')
    )

def create_analytics_tables(**context):
    """Create analytics tables if not exist"""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    # Daily sales summary
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_sales_summary (
            report_date DATE PRIMARY KEY,
            total_orders INT DEFAULT 0,
            completed_orders INT DEFAULT 0,
            total_revenue DECIMAL(15,2) DEFAULT 0.00,
            total_items_sold INT DEFAULT 0,
            unique_customers INT DEFAULT 0,
            avg_order_value DECIMAL(10,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Product performance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_performance (
            report_date DATE,
            product_id INT,
            product_name VARCHAR(100),
            times_ordered INT DEFAULT 0,
            total_quantity INT DEFAULT 0,
            total_revenue DECIMAL(15,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (report_date, product_id)
        )
    """)
    
    # Store performance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_performance (
            report_date DATE,
            store_id INT,
            store_name VARCHAR(100),
            total_orders INT DEFAULT 0,
            total_revenue DECIMAL(15,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (report_date, store_id)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ Analytics tables created/verified")
    return True

def generate_daily_sales(**context):
    """Generate daily sales summary for yesterday"""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    target_date = (datetime.now() - timedelta(days=1)).date()
    
    cursor.execute("""
        INSERT INTO daily_sales_summary 
        (report_date, total_orders, completed_orders, total_revenue, total_items_sold, unique_customers, avg_order_value)
        SELECT 
            DATE(o.order_date) as report_date,
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(CASE WHEN o.order_status = '4' THEN 1 ELSE 0 END) as completed_orders,
            COALESCE(SUM(oi.quantity * oi.list_price * (1 - oi.discount/100)), 0) as total_revenue,
            COALESCE(SUM(oi.quantity), 0) as total_items_sold,
            COUNT(DISTINCT o.customer_id) as unique_customers,
            COALESCE(SUM(oi.quantity * oi.list_price * (1 - oi.discount/100)) / COUNT(DISTINCT o.order_id), 0) as avg_order_value
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE DATE(o.order_date) = %s
        GROUP BY DATE(o.order_date)
        ON DUPLICATE KEY UPDATE
            total_orders = VALUES(total_orders),
            completed_orders = VALUES(completed_orders),
            total_revenue = VALUES(total_revenue),
            total_items_sold = VALUES(total_items_sold),
            unique_customers = VALUES(unique_customers),
            avg_order_value = VALUES(avg_order_value),
            created_at = CURRENT_TIMESTAMP
    """, (target_date,))
    
    rows = cursor.rowcount
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Generated daily sales summary for {target_date}")
    return rows

def generate_product_performance(**context):
    """Generate product performance metrics"""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    target_date = (datetime.now() - timedelta(days=1)).date()
    
    cursor.execute("""
        INSERT INTO product_performance 
        (report_date, product_id, product_name, times_ordered, total_quantity, total_revenue)
        SELECT 
            DATE(o.order_date) as report_date,
            p.product_id,
            p.product_name,
            COUNT(DISTINCT o.order_id) as times_ordered,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.quantity * oi.list_price * (1 - oi.discount/100)) as total_revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE DATE(o.order_date) = %s
        GROUP BY DATE(o.order_date), p.product_id, p.product_name
        ON DUPLICATE KEY UPDATE
            times_ordered = VALUES(times_ordered),
            total_quantity = VALUES(total_quantity),
            total_revenue = VALUES(total_revenue),
            created_at = CURRENT_TIMESTAMP
    """, (target_date,))
    
    rows = cursor.rowcount
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Generated product performance for {target_date}: {rows} products")
    return rows

def generate_store_performance(**context):
    """Generate store performance metrics"""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    target_date = (datetime.now() - timedelta(days=1)).date()
    
    cursor.execute("""
        INSERT INTO store_performance 
        (report_date, store_id, store_name, total_orders, total_revenue)
        SELECT 
            DATE(o.order_date) as report_date,
            s.store_id,
            s.store_name,
            COUNT(DISTINCT o.order_id) as total_orders,
            COALESCE(SUM(oi.quantity * oi.list_price * (1 - oi.discount/100)), 0) as total_revenue
        FROM orders o
        JOIN stores s ON o.store_id = s.store_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE DATE(o.order_date) = %s
        GROUP BY DATE(o.order_date), s.store_id, s.store_name
        ON DUPLICATE KEY UPDATE
            total_orders = VALUES(total_orders),
            total_revenue = VALUES(total_revenue),
            created_at = CURRENT_TIMESTAMP
    """, (target_date,))
    
    rows = cursor.rowcount
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Generated store performance for {target_date}: {rows} stores")
    return rows

with DAG(
    'dag_analytics',
    default_args=default_args,
    description='Generate bike store analytics and KPIs',
    schedule='0 2 * * *',
    catchup=False,
    tags=['analytics', 'reporting', 'kpi'],
) as dag:
    
    task_create_tables = PythonOperator(
        task_id='create_analytics_tables',
        python_callable=create_analytics_tables,
    )
    
    task_daily_sales = PythonOperator(
        task_id='generate_daily_sales',
        python_callable=generate_daily_sales,
    )
    
    task_product_perf = PythonOperator(
        task_id='generate_product_performance',
        python_callable=generate_product_performance,
    )
    
    task_store_perf = PythonOperator(
        task_id='generate_store_performance',
        python_callable=generate_store_performance,
    )
    
    # Sequential execution
    task_create_tables >> [task_daily_sales, task_product_perf, task_store_perf]