-- Изменение статуса заказа (нужно обновить в двух таблицах — денормализация!)
UPDATE orders_by_customer
SET status = 'SHIPPED'
WHERE customer_id = 'cust-001' AND order_date = '2026-10-05' AND order_id = 'ord-1042';

-- В orders_by_status статус — partition key, поэтому DELETE + INSERT
DELETE FROM orders_by_status
WHERE status = 'PROCESSING' AND order_date = '2026-10-05' AND order_id = 'ord-1042';

INSERT INTO orders_by_status (status, order_date, order_id, customer_id, total_amount)
VALUES ('SHIPPED', '2026-10-05', 'ord-1042', 'cust-001', 3200.00);

-- Безопасное удаление одной позиции
DELETE FROM order_items
WHERE order_id = 'ord-1001' AND product_id = 'prod-310';