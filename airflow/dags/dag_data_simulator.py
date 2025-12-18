from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mysql.connector
import random
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
    """Create MySQL connection to pipeline_data database"""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'mysql-dev'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'airflow_user'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('PIPELINE_DATABASE', 'pipeline_data')
    )

def simulate_new_customers(**context):
    """Generate new customers"""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    # Get max customer_id
    cursor.execute("SELECT COALESCE(MAX(customer_id), 0) FROM customers")
    max_id = cursor.fetchone()[0]
    
    first_names = ['John', 'Emma', 'Michael', 'Sophia', 'William', 'Olivia', 'James', 'Ava']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia']
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA']
    
    num_customers = random.randint(5, 15)
    inserted = 0
    
    for i in range(num_customers):
        customer_id = max_id + i + 1
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        phone = f"+1-555-{random.randint(1000, 9999)}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@email.com"
        city_idx = random.randint(0, len(cities) - 1)
        
        try:
            cursor.execute("""
                INSERT INTO customers 
                (customer_id, first_name, last_name, phone, email, street, city, state, zip_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                customer_id, first_name, last_name, phone, email,
                f"{random.randint(100, 9999)} Main St",
                cities[city_idx], states[city_idx],
                f"{random.randint(10000, 99999)}"
            ))
            inserted += 1
        except mysql.connector.Error as e:
            print(f"Error inserting customer: {e}")
            continue
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Created {inserted} new customers")
    return inserted

def simulate_orders(**context):
    """Generate new orders with order_items"""
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get max order_id
    cursor.execute("SELECT COALESCE(MAX(order_id), 0) FROM orders")
    max_order_id = cursor.fetchone()['COALESCE(MAX(order_id), 0)']
    
    # Get random customers, stores, staff, products
    cursor.execute("SELECT customer_id FROM customers ORDER BY RAND() LIMIT 10")
    customers = [row['customer_id'] for row in cursor.fetchall()]
    
    cursor.execute("SELECT store_id FROM stores LIMIT 5")
    stores = [row['store_id'] for row in cursor.fetchall()]
    
    cursor.execute("SELECT staff_id, store_id FROM staffs WHERE active = 1 LIMIT 10")
    staff_list = cursor.fetchall()
    
    cursor.execute("SELECT product_id, list_price FROM products LIMIT 50")
    products = cursor.fetchall()
    
    if not customers or not stores or not staff_list or not products:
        print("⚠️  Missing reference data (customers/stores/staff/products)")
        cursor.close()
        conn.close()
        return 0
    
    num_orders = random.randint(10, 30)
    order_statuses = ['1', '2', '3', '4']
    inserted_orders = 0
    
    for i in range(num_orders):
        order_id = max_order_id + i + 1
        customer_id = random.choice(customers)
        store_id = random.choice(stores)
        
        store_staff = [s for s in staff_list if s['store_id'] == store_id]
        if not store_staff:
            store_staff = staff_list
        staff_id = random.choice(store_staff)['staff_id']
        
        order_status = random.choice(order_statuses)
        order_date = datetime.now() - timedelta(days=random.randint(0, 30))
        required_date = order_date + timedelta(days=random.randint(3, 14))
        shipped_date = order_date + timedelta(days=random.randint(1, 7)) if order_status == '4' else None
        
        try:
            cursor.execute("""
                INSERT INTO orders 
                (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id))
            
            num_items = random.randint(1, 5)
            for item_num in range(1, num_items + 1):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                discount = random.choice([0, 5, 10, 15, 20])
                
                cursor.execute("""
                    INSERT INTO order_items 
                    (order_id, item_id, product_id, quantity, list_price, discount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (order_id, item_num, product['product_id'], quantity, product['list_price'], discount))
            
            inserted_orders += 1
            
        except mysql.connector.Error as e:
            print(f"Error inserting order {order_id}: {e}")
            continue
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Created {inserted_orders} new orders")
    return inserted_orders

def update_stock_levels(**context):
    """Randomly update stock quantities"""
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get random stocks to update
    cursor.execute("""
        SELECT store_id, product_id, quantity 
        FROM stocks 
        ORDER BY RAND() 
        LIMIT 20
    """)
    stocks = cursor.fetchall()
    
    updated = 0
    for stock in stocks:
        change = random.randint(-10, 50)
        new_quantity = max(0, stock['quantity'] + change)
        
        cursor.execute("""
            UPDATE stocks 
            SET quantity = %s 
            WHERE store_id = %s AND product_id = %s
        """, (new_quantity, stock['store_id'], stock['product_id']))
        updated += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Updated {updated} stock levels")
    return updated

with DAG(
    'dag_data_simulator',
    default_args=default_args,
    description='Generate synthetic bike store data',
    schedule_interval='*/15 * * * *',
    catchup=False,
    tags=['data-generation', 'bike-store'],
) as dag:
    
    task_customers = PythonOperator(
        task_id='generate_customers',
        python_callable=simulate_new_customers,
    )
    
    task_orders = PythonOperator(
        task_id='generate_orders',
        python_callable=simulate_orders,
    )
    
    task_stocks = PythonOperator(
        task_id='update_stock_levels',
        python_callable=update_stock_levels,
    )
    
    # Run in parallel
    [task_customers, task_orders, task_stocks]