-- =====================================================
-- Лабораторная работа № 6 — Вариант 2: Интернет-магазин
-- =====================================================

CREATE KEYSPACE IF NOT EXISTS lab6_shop
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

USE lab6_shop;

-- 1. Заказы клиента (основная таблица чтения)
CREATE TABLE IF NOT EXISTS orders_by_customer (
    customer_id     text,
    order_date      date,
    order_id        text,
    status          text,
    total_amount    decimal,
    items_count     int,
    PRIMARY KEY ((customer_id), order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC, order_id ASC);

-- 2. Позиции заказа
CREATE TABLE IF NOT EXISTS order_items (
    order_id        text,
    product_id      text,
    product_name    text,
    quantity        int,
    price           decimal,
    PRIMARY KEY ((order_id), product_id)
);

-- 3. Заказы по статусу (для менеджеров / аналитики)
CREATE TABLE IF NOT EXISTS orders_by_status (
    status          text,
    order_date      date,
    order_id        text,
    customer_id     text,
    total_amount    decimal,
    PRIMARY KEY ((status), order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC, order_id ASC);