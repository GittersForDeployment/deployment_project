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

def validate_customer_data(**context):
    """Validate and clean customer records"""
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Find customers with invalid data
    cursor.execute("""
        SELECT customer_id, first_name, last_name, phone, email 
        FROM customers 
        WHERE email NOT LIKE '%@%' 
           OR first_name IS NULL 
           OR last_name IS NULL
        LIMIT 100
    """)
    
    invalid_customers = cursor.fetchall()
    fixed = 0
    flagged = 0
    
    for customer in invalid_customers:
        # Fix invalid emails
        if '@' not in customer['email']:
            new_email = f"{customer['first_name'].lower()}.{customer['last_name'].lower()}@fixed.com"
            cursor.execute("""
                UPDATE customers 
                SET email = %s 
                WHERE customer_id = %s
            """, (new_email, customer['customer_id']))
            fixed += 1
        else:
            flagged += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Fixed {fixed} customers, flagged {flagged} for review")
    return {'fixed': fixed, 'flagged': flagged}

def validate_orders(**context):
    """Validate order logic and dates"""
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Find orders with invalid dates (shipped before ordered)
    cursor.execute("""
        SELECT order_id, order_date, shipped_date 
        FROM orders 
        WHERE shipped_date IS NOT NULL 
          AND shipped_date < order_date
        LIMIT 100
    """)
    
    invalid_orders = cursor.fetchall()
    fixed = 0
    
    for order in invalid_orders:
        # Fix by setting shipped_date = order_date + 1 day
        cursor.execute("""
            UPDATE orders 
            SET shipped_date = DATE_ADD(order_date, INTERVAL 1 DAY)
            WHERE order_id = %s
        """, (order['order_id'],))
        fixed += 1
    
    # Find orders with status '4' (completed) but no shipped_date
    cursor.execute("""
        SELECT order_id, order_date 
        FROM orders 
        WHERE order_status = '4' AND shipped_date IS NULL
        LIMIT 100
    """)
    
    incomplete_shipments = cursor.fetchall()
    
    for order in incomplete_shipments:
        cursor.execute("""
            UPDATE orders 
            SET shipped_date = DATE_ADD(order_date, INTERVAL 2 DAY)
            WHERE order_id = %s
        """, (order['order_id'],))
        fixed += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Fixed {fixed} order date issues")
    return fixed

def check_negative_stock(**context):
    """Detect and fix negative stock levels"""
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT store_id, product_id, quantity 
        FROM stocks 
        WHERE quantity < 0
    """)
    
    negative_stocks = cursor.fetchall()
    fixed = 0
    
    for stock in negative_stocks:
        cursor.execute("""
            UPDATE stocks 
            SET quantity = 0 
            WHERE store_id = %s AND product_id = %s
        """, (stock['store_id'], stock['product_id']))
        fixed += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Fixed {fixed} negative stock levels")
    return fixed

def clean_duplicate_orders(**context):
    """Remove duplicate order items"""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    # Find duplicate order_items (same order_id + product_id)
    cursor.execute("""
        SELECT order_id, product_id, COUNT(*) as cnt
        FROM order_items
        GROUP BY order_id, product_id
        HAVING COUNT(*) > 1
    """)
    
    duplicates = cursor.fetchall()
    removed = 0
    
    for dup in duplicates:
        order_id, product_id, count = dup
        # Keep only the first item, delete others
        cursor.execute("""
            DELETE FROM order_items 
            WHERE order_id = %s AND product_id = %s AND item_id > (
                SELECT MIN(item_id) FROM (
                    SELECT item_id FROM order_items 
                    WHERE order_id = %s AND product_id = %s
                ) tmp
            )
        """, (order_id, product_id, order_id, product_id))
        removed += count - 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Removed {removed} duplicate order items")
    return removed

with DAG(
    'dag_data_cleaning',
    default_args=default_args,
    description='Clean and validate bike store data',
    schedule='0 */2 * * *',  # Every 2 hours
    catchup=False,
    tags=['data-cleaning', 'validation'],
) as dag:
    
    task_validate_customers = PythonOperator(
        task_id='validate_customer_data',
        python_callable=validate_customer_data,
    )
    
    task_validate_orders = PythonOperator(
        task_id='validate_orders',
        python_callable=validate_orders,
    )
    
    task_check_stock = PythonOperator(
        task_id='check_negative_stock',
        python_callable=check_negative_stock,
    )
    
    task_clean_duplicates = PythonOperator(
        task_id='clean_duplicate_orders',
        python_callable=clean_duplicate_orders,
    )
    
    # Sequential execution
    task_validate_customers >> task_validate_orders >> task_check_stock >> task_clean_duplicates