CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE brands (
    brand_id INT PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    brand_id INT NOT NULL,
    category_id INT NOT NULL,
    model_year SMALLINT CHECK (model_year >= 1900),
    list_price DECIMAL(10,2) CHECK (list_price >= 0),
    CONSTRAINT fk_product_brand FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    CONSTRAINT fk_product_category FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(50) CHECK (LENGTH(phone) <= 50),
    email VARCHAR(100) CHECK (email LIKE '%_@_%._%'),
    street VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20)
);

CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    phone VARCHAR(50) CHECK (LENGTH(phone) <= 50),
    email VARCHAR(100) CHECK (email LIKE '%_@_%._%'),
    street VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20)
);

CREATE TABLE staffs (
    staff_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) CHECK (email LIKE '%_@_%._%'),
    phone VARCHAR(50) CHECK (LENGTH(phone) <= 50),
    active TINYINT(1) DEFAULT 1 CHECK (active IN (0,1)),
    store_id INT NOT NULL,
    manager_id INT,
    CONSTRAINT fk_staff_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
    CONSTRAINT fk_staff_manager FOREIGN KEY (manager_id) REFERENCES staffs(staff_id)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_status CHAR(1) DEFAULT '1' CHECK (order_status IN ('1','2','3','4')),
    order_date DATE DEFAULT (CURDATE()),
    required_date DATE,
    shipped_date DATE,
    store_id INT NOT NULL,
    staff_id INT NOT NULL,
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_order_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
    CONSTRAINT fk_order_staff FOREIGN KEY (staff_id) REFERENCES staffs(staff_id),
    CONSTRAINT chk_order_dates CHECK (shipped_date IS NULL OR shipped_date >= order_date)
);

CREATE TABLE order_items (
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT CHECK (quantity > 0),
    list_price DECIMAL(10,2) CHECK (list_price >= 0),
    discount DECIMAL(5,2) CHECK (discount >= 0 AND discount <= 100),
    PRIMARY KEY (order_id, item_id),
    CONSTRAINT fk_orderitem_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_orderitem_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE stocks (
    store_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT CHECK (quantity >= 0),
    PRIMARY KEY (store_id, product_id),
    CONSTRAINT fk_stock_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
    CONSTRAINT fk_stock_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);
