USE pipeline_data;

INSERT INTO brands (brand_id, brand_name) 
VALUES
    (1, 'Electra'),
    (2, 'Haro'),
    (3, 'Heller'),
    (4, 'Pure Cycles'),
    (5, 'Ritchey'),
    (6, 'Strider'),
    (7, 'Sun Bicycles'),
    (8, 'Surly'),
    (9, 'Trek');

INSERT INTO categories (category_id, category_name) 
VALUES
    (1, 'Children Bicycles'),
    (2, 'Comfort Bicycles'),
    (3, 'Cruisers Bicycles'),
    (4, 'Cyclocross Bicycles'),
    (5, 'Electric Bikes'),
    (6, 'Mountain Bikes'),
    (7, 'Road Bikes');

INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) 
VALUES
    (1, 'Debra', 'Burks', NULL, 'debra.burks@yahoo.com', '9273 Thorne Ave. ', 'Orchard Park', 'NY', '14127'),
    (2, 'Kasha', 'Todd', NULL, 'kasha.todd@yahoo.com', '910 Vine Street ', 'Campbell', 'CA', '95008'),
    (3, 'Tameka', 'Fisher', NULL, 'tameka.fisher@aol.com', '769C Honey Creek St. ', 'Redondo Beach', 'CA', '90278'),
    (4, 'Daryl', 'Spence', NULL, 'daryl.spence@aol.com', '988 Pearl Lane ', 'Uniondale', 'NY', '11553'),
    (5, 'Charolette', 'Rice', '(916) 381-6003', 'charolette.rice@msn.com', '107 River Dr. ', 'Sacramento', 'CA', '95820'),
    (6, 'Lyndsey', 'Bean', NULL, 'lyndsey.bean@hotmail.com', '769 West Road ', 'Fairport', 'NY', '14450'),
    (7, 'Latasha', 'Hays', '(716) 986-3359', 'latasha.hays@hotmail.com', '7014 Manor Station Rd. ', 'Buffalo', 'NY', '14215'),
    (8, 'Jacquline', 'Duncan', NULL, 'jacquline.duncan@yahoo.com', '15 Brown St. ', 'Jackson Heights', 'NY', '11372'),
    (9, 'Genoveva', 'Baldwin', NULL, 'genoveva.baldwin@msn.com', '8550 Spruce Drive ', 'Port Washington', 'NY', '11050'),
    (10, 'Pamelia', 'Newman', NULL, 'pamelia.newman@gmail.com', '476 Chestnut Ave. ', 'Monroe', 'NY', '10950');

INSERT INTO stores (store_id, store_name, phone, email, street, city, state, zip_code) 
VALUES 
    (1, 'Santa Cruz Bikes', '(831) 476-4321', 'santacruz@bikes.shop', '3700 Portola Drive', 'Santa Cruz', 'CA', '95060'),
    (2, 'Baldwin Bikes', '(516) 379-8888', 'baldwin@bikes.shop', '4200 Chestnut Lane', 'Baldwin', 'NY', '11432'),
    (3, 'Rowlett Bikes', '(972) 530-5555', 'rowlett@bikes.shop', '8000 Fairway Avenue', 'Rowlett', 'TX', '75088');

INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) 
VALUES 
    (1, 'Fabiola', 'Jackson', 'fabiola.jackson@bikes.shop', '(831) 555-5554', 1, 1, NULL),
    (2, 'Mireya', 'Copeland', 'mireya.copeland@bikes.shop', '(831) 555-5555', 1, 1, 1),
    (3, 'Genna', 'Serrano', 'genna.serrano@bikes.shop', '(831) 555-5556', 1, 1, 2),
    (4, 'Virgie', 'Wiggins', 'virgie.wiggins@bikes.shop', '(831) 555-5557', 1, 1, 2),
    (5, 'Jannette', 'David', 'jannette.david@bikes.shop', '(516) 379-4444', 1, 2, 1),
    (6, 'Marcelene', 'Boyer', 'marcelene.boyer@bikes.shop', '(516) 379-4445', 1, 2, 5),
    (7, 'Venita', 'Daniel', 'venita.daniel@bikes.shop', '(516) 379-4446', 1, 2, 5),
    (8, 'Kali', 'Vargas', 'kali.vargas@bikes.shop', '(972) 530-5555', 1, 3, 1),
    (9, 'Layla', 'Terrell', 'layla.terrell@bikes.shop', '(972) 530-5556', 1, 3, 7),
    (10, 'Bernardine', 'Houston', 'bernardine.houston@bikes.shop', '(972) 530-5557', 1, 3, 7);

INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) 
VALUES
    (1, 'Trek 820 - 2016', 9, 6, 2016, 379.99),
    (2, 'Ritchey Timberwolf Frameset - 2016', 5, 6, 2016, 749.99),
    (3, 'Surly Wednesday Frameset - 2016', 8, 6, 2016, 999.99),
    (4, 'Trek Fuel EX 8 29 - 2016', 9, 6, 2016, 2899.99),
    (5, 'Heller Shagamaw Frame - 2016', 3, 6, 2016, 1320.99),
    (6, 'Surly Ice Cream Truck Frameset - 2016', 8, 6, 2016, 469.99),
    (7, 'Trek Slash 8 27.5 - 2016', 9, 6, 2016, 3999.99),
    (8, 'Trek Remedy 29 Carbon Frameset - 2016', 9, 6, 2016, 1799.99),
    (9, 'Trek Conduit+ - 2016', 9, 5, 2016, 2999.99),
    (10, 'Surly Straggler - 2016', 8, 4, 2016, 1549);

INSERT INTO stocks (store_id, product_id, quantity) 
VALUES 
    (1, 1, 27),
    (1, 2, 5),
    (1, 3, 6),
    (1, 4, 23),
    (1, 5, 22),
    (1, 6, 0),
    (1, 7, 8),
    (1, 8, 0),
    (1, 9, 11),
    (1, 10, 15),
    (2, 1, 15),
    (2, 2, 10),
    (2, 3, 8),
    (2, 4, 12),
    (2, 5, 18),
    (3, 1, 20),
    (3, 2, 7),
    (3, 3, 9);

INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) 
VALUES 
    (1, 1, '4', '2016-01-01', '2016-01-03', '2016-01-03', 1, 2),
    (2, 2, '4', '2016-01-01', '2016-01-04', '2016-01-03', 2, 6),
    (3, 3, '4', '2016-01-02', '2016-01-05', '2016-01-03', 2, 7),
    (4, 4, '4', '2016-01-03', '2016-01-04', '2016-01-05', 1, 3),
    (5, 5, '4', '2016-01-03', '2016-01-06', '2016-01-06', 2, 6),
    (6, 6, '4', '2016-01-04', '2016-01-07', '2016-01-05', 2, 6),
    (7, 7, '4', '2016-01-04', '2016-01-07', '2016-01-05', 2, 6),
    (8, 8, '4', '2016-01-04', '2016-01-05', '2016-01-05', 2, 7),
    (9, 9, '4', '2016-01-05', '2016-01-08', '2016-01-08', 1, 2),
    (10, 10, '4', '2016-01-05', '2016-01-06', '2016-01-06', 2, 6);

INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) 
VALUES 
    (1, 1, 1, 1, 379.99, 0.2),
    (1, 2, 8, 2, 1799.99, 0.07),
    (1, 3, 10, 2, 1549, 0.05),
    (2, 1, 2, 1, 749.99, 0.07),
    (2, 2, 3, 2, 999.99, 0.05),
    (3, 1, 3, 1, 999.99, 0.05),
    (3, 2, 1, 1, 379.99, 0.05),
    (4, 1, 2, 2, 749.99, 0.1),
    (5, 1, 4, 1, 2899.99, 0.15),
    (6, 1, 5, 1, 1320.99, 0.1);