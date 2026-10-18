import time
from datetime import datetime, timedelta
from src.database import DatabaseConnection
from src.models import WarehouseOperationService

def create_keyspace_and_tables(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS warehouse_db 
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """)
    session.execute("USE warehouse_db;")

    session.execute("""
                    CREATE TABLE IF NOT EXISTS operations_by_warehouse_date (
                                                                                warehouse_id text,
                                                                                date text,
                                                                                operation_time timestamp,
                                                                                operation_id timeuuid,
                                                                                item_id text,
                                                                                operation_type text,
                                                                                quantity int,
                                                                                operator text,
                                                                                notes text,
                                                                                PRIMARY KEY ((warehouse_id, date), operation_time, operation_id)
                        ) WITH CLUSTERING ORDER BY (operation_time DESC, operation_id DESC);
                    """)

    session.execute("""
                    CREATE TABLE IF NOT EXISTS operations_by_item (
                                                                      item_id text,
                                                                      warehouse_id text,
                                                                      operation_time timestamp,
                                                                      operation_id timeuuid,
                                                                      date text,
                                                                      operation_type text,
                                                                      quantity int,
                                                                      operator text,
                                                                      notes text,
                                                                      PRIMARY KEY ((item_id), warehouse_id, operation_time, operation_id)
                        ) WITH CLUSTERING ORDER BY (warehouse_id ASC, operation_time DESC, operation_id DESC);
                    """)
    print("Keyspace и таблицы успешно созданы/проверены.")

def seed():
    session = DatabaseConnection.get_session()
    create_keyspace_and_tables(session)
    service = WarehouseOperationService()

    warehouses = ["WH-Almaty-01", "WH-Astana-02"]
    items = ["ITEM-9901", "ITEM-9902", "ITEM-9903", "ITEM-9904"]
    op_types = ["IN", "OUT", "ADJUSTMENT", "TRANSFER"]
    operators = ["Иван П.", "Айдын С.", "Елена К.", "Марат Б."]

    print("Генерация 30 синтетических записей...")
    base_time = datetime.now() - timedelta(hours=5)

    for i in range(35):
        wh = warehouses[i % len(warehouses)]
        item = items[i % len(items)]
        op_type = op_types[i % len(op_types)]
        qty = (i + 1) * 5
        op = operators[i % len(operators)]
        op_time = base_time + timedelta(minutes=i * 8)

        service.record_operation(
            warehouse_id=wh,
            item_id=item,
            operation_type=op_type,
            quantity=qty,
            operator=op,
            notes=f"Автоматическая операция # {i+1}"
        )

    print("Генерация завершена! Создано 35 записей.")
    DatabaseConnection.close()

if __name__ == "__main__":
    seed()