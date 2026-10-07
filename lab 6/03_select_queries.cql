-- Q1. Все заказы клиента (новые сверху)
SELECT * FROM orders_by_customer WHERE customer_id = 'cust-001';

-- Q2. Заказы клиента за период
SELECT * FROM orders_by_customer
WHERE customer_id = 'cust-001'
  AND order_date >= '2026-09-20'
  AND order_date <= '2026-10-05';

-- Q3. Позиции заказа
SELECT * FROM order_items WHERE order_id = 'ord-1030';

-- Q4. Последние 3 заказа клиента
SELECT * FROM orders_by_customer WHERE customer_id = 'cust-003' LIMIT 3;

-- Q5. Все заказы в статусе PROCESSING (новые сверху)
SELECT * FROM orders_by_status WHERE status = 'PROCESSING';