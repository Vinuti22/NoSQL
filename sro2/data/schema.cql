CREATE KEYSPACE IF NOT EXISTS warehouse
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- AP1-AP4: операции склада за день (партиция = склад + день)
CREATE TABLE IF NOT EXISTS warehouse.movements_by_warehouse_day (
    warehouse_id  text,
    day           date,
    ts            timestamp,
    movement_id   uuid,
    product_id    text,
    movement_type text,      -- IN | OUT | TRANSFER | ADJUST
    quantity      int,
    operator      text,
    doc_ref       text,
    comment       text,
    PRIMARY KEY ((warehouse_id, day), ts, movement_id)
) WITH CLUSTERING ORDER BY (ts DESC, movement_id ASC);

-- AP5-AP8: история товара (партиция = товар + месяц, ограничивает рост партиции)
CREATE TABLE IF NOT EXISTS warehouse.movements_by_product (
    product_id    text,
    year_month    text,      -- 'YYYY-MM'
    ts            timestamp,
    movement_id   uuid,
    warehouse_id  text,
    movement_type text,
    quantity      int,
    operator      text,
    doc_ref       text,
    comment       text,
    PRIMARY KEY ((product_id, year_month), ts, movement_id)
) WITH CLUSTERING ORDER BY (ts DESC, movement_id ASC);
