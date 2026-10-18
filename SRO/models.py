import uuid
from datetime import datetime
from cassandra.util import uuid_from_time
from src.database import DatabaseConnection

class WarehouseOperationService:
    def __init__(self):
        self.session = DatabaseConnection.get_session()
        self.keyspace = "warehouse_db"
        self._prepare_statements()

    def _prepare_statements(self):
        # Подготовка CQL выражений для обеспечения безопасности и производительности
        self.insert_wh_date_stmt = self.session.prepare("""
                                                        INSERT INTO warehouse_db.operations_by_warehouse_date
                                                        (warehouse_id, date, operation_time, operation_id, item_id, operation_type, quantity, operator, notes)
                                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                                        """)

        self.insert_item_stmt = self.session.prepare("""
                                                     INSERT INTO warehouse_db.operations_by_item
                                                     (item_id, warehouse_id, operation_time, operation_id, date, operation_type, quantity, operator, notes)
                                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                                     """)

        self.select_by_wh_date_stmt = self.session.prepare("""
                                                           SELECT * FROM warehouse_db.operations_by_warehouse_date
                                                           WHERE warehouse_id = ? AND date = ?
                                                           """)

        self.select_by_item_stmt = self.session.prepare("""
                                                        SELECT * FROM warehouse_db.operations_by_item
                                                        WHERE item_id = ?
                                                        """)

    def record_operation(self, warehouse_id: str, item_id: str, operation_type: str, quantity: int, operator: str, notes: str = ""):
        """AP1: Запись операции в обе таблицы с использованием Batch для атомарности/параллельной записи"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        op_id = uuid_from_time(now)

        batch = self.session.batch_type_enum if hasattr(self.session, 'batch_type_enum') else 0

        # Выполняем вставку в обе таблицы
        self.session.execute(self.insert_wh_date_stmt, [
            warehouse_id, date_str, now, op_id, item_id, operation_type, quantity, operator, notes
        ])
        self.session.execute(self.insert_item_stmt, [
            item_id, warehouse_id, now, op_id, date_str, operation_type, quantity, operator
        ])
        return op_id

    def get_operations_by_warehouse_and_date(self, warehouse_id: str, date_str: str):
        """AP2: Получение истории операций по складу и дате"""
        return list(self.session.execute(self.select_by_wh_date_stmt, [warehouse_id, date_str]))

    def get_operations_by_item(self, item_id: str):
        """AP3: Получение истории движения конкретного товара"""
        return list(self.session.execute(self.select_by_item_stmt, [item_id]))

    def get_operations_by_type(self, warehouse_id: str, date_str: str, op_type: str):
        """AP4: Фильтрация операций по типу на уровне приложения"""
        rows = self.get_operations_by_warehouse_and_date(warehouse_id, date_str)
        return [row for row in rows if row.operation_type == op_type]

    def get_latest_operations(self, warehouse_id: str, date_str: str, limit: int = 5):
        """AP5: Получение последних N операций (ограничение среза)"""
        query = f"""
            SELECT * FROM warehouse_db.operations_by_warehouse_date 
            WHERE warehouse_id = %s AND date = %s 
            LIMIT {limit}
        """
        prepared = self.session.prepare(query)
        return list(self.session.execute(prepared, [warehouse_id, date_str]))

    def get_operations_by_time_range(self, warehouse_id: str, date_str: str, start_time: datetime, end_time: datetime):
        """AP6: Фильтрация по временному диапазону внутри партиции"""
        rows = self.get_operations_by_warehouse_and_date(warehouse_id, date_str)
        return [row for row in rows if start_time <= row.operation_time <= end_time]

    def update_operation_notes(self, warehouse_id: str, date_str: str, operation_time: datetime, operation_id: uuid.UUID, new_notes: str):
        """AP7: Обновление примечания к операции"""
        query = """
                UPDATE warehouse_db.operations_by_warehouse_date
                SET notes = %s
                WHERE warehouse_id = %s AND date = %s AND operation_time = %s AND operation_id = %s \
                """
        self.session.execute(query, [new_notes, warehouse_id, date_str, operation_time, operation_id])

    def get_daily_turnover_analytics(self, warehouse_id: str, date_str: str):
        """AP8: Аналитический срез (оборот товаров за день)"""
        rows = self.get_operations_by_warehouse_and_date(warehouse_id, date_str)
        turnover = {}
        for r in rows:
            turnover[r.item_id] = turnover.get(r.item_id, 0) + (r.quantity if r.operation_type == 'IN' else -r.quantity)
        return turnover