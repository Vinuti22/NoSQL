-- ========== Заказы клиентов ==========
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-001', '2026-09-15', 'ord-1001', 'DELIVERED', 12500.00, 3);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-001', '2026-09-28', 'ord-1015', 'DELIVERED', 8900.00, 2);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-001', '2026-10-02', 'ord-1030', 'SHIPPED', 15600.00, 4);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-001', '2026-10-05', 'ord-1042', 'PROCESSING', 3200.00, 1);

INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-002', '2026-09-20', 'ord-1008', 'DELIVERED', 4500.00, 2);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-002', '2026-10-01', 'ord-1025', 'CANCELLED', 7800.00, 3);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-002', '2026-10-06', 'ord-1048', 'PROCESSING', 11200.00, 5);

INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-003', '2026-09-10', 'ord-0990', 'DELIVERED', 21000.00, 6);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-003', '2026-09-25', 'ord-1010', 'DELIVERED', 6700.00, 2);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-003', '2026-10-03', 'ord-1035', 'SHIPPED', 9800.00, 3);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-003', '2026-10-07', 'ord-1050', 'PROCESSING', 4300.00, 1);

INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-004', '2026-09-18', 'ord-1005', 'DELIVERED', 15000.00, 4);
INSERT INTO orders_by_customer (customer_id, order_date, order_id, status, total_amount, items_count)
VALUES ('cust-004', '2026-10-04', 'ord-1040', 'SHIPPED', 7200.00, 2);

-- ========== Позиции заказов ==========
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1001', 'prod-101', 'Ноутбук ASUS', 1, 9500.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1001', 'prod-205', 'Мышь Logitech', 1, 1500.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1001', 'prod-310', 'Коврик', 1, 1500.00);

INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1015', 'prod-150', 'Наушники Sony', 1, 6900.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1015', 'prod-220', 'Чехол', 1, 2000.00);

INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1030', 'prod-101', 'Ноутбук ASUS', 1, 9500.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1030', 'prod-180', 'Монитор 27"', 1, 4500.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1030', 'prod-205', 'Мышь Logitech', 1, 1500.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1030', 'prod-310', 'Коврик', 1, 100.00);

INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1042', 'prod-250', 'Клавиатура механическая', 1, 3200.00);

INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1008', 'prod-300', 'Флешка 128GB', 2, 2250.00);

INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1025', 'prod-101', 'Ноутбук ASUS', 1, 9500.00);  -- будет отменён

INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1048', 'prod-180', 'Монитор 27"', 1, 4500.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1048', 'prod-205', 'Мышь Logitech', 2, 1500.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1048', 'prod-250', 'Клавиатура', 1, 3200.00);
INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
('ord-1048', 'prod-310', 'Коврик', 1, 500.00);

-- ========== Заказы по статусу ==========
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('DELIVERED', '2026-09-15', 'ord-1001', 'cust-001', 12500.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('DELIVERED', '2026-09-28', 'ord-1015', 'cust-001', 8900.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('SHIPPED', '2026-10-02', 'ord-1030', 'cust-001', 15600.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('PROCESSING', '2026-10-05', 'ord-1042', 'cust-001', 3200.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('DELIVERED', '2026-09-20', 'ord-1008', 'cust-002', 4500.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('CANCELLED', '2026-10-01', 'ord-1025', 'cust-002', 7800.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('PROCESSING', '2026-10-06', 'ord-1048', 'cust-002', 11200.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('DELIVERED', '2026-09-10', 'ord-0990', 'cust-003', 21000.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('DELIVERED', '2026-09-25', 'ord-1010', 'cust-003', 6700.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('SHIPPED', '2026-10-03', 'ord-1035', 'cust-003', 9800.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('PROCESSING', '2026-10-07', 'ord-1050', 'cust-003', 4300.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('DELIVERED', '2026-09-18', 'ord-1005', 'cust-004', 15000.00);
INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount) VALUES
('SHIPPED', '2026-10-04', 'ord-1040', 'cust-004', 7200.00);