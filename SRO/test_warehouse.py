import pytest
from datetime import datetime
from src.database import DatabaseConnection
from src.models import WarehouseOperationService

@pytest.fixture(scope="module")
def db_setup():
    # Инициализация подключения для тестов
    session = DatabaseConnection.get_session()
    yield session
    DatabaseConnection.close()

def test_record_and_fetch_operation(db_setup):
    service = WarehouseOperationService()
    today_str = datetime.now().strftime("%Y-%m-%d")
    wh_test = "WH-Test-Warehouse"
    item_test = "ITEM-TEST-1"

    # Запись
    op_id = service.record_operation(
        warehouse_id=wh_test,
        item_id=item_test,
        operation_type="IN",
        quantity=100,
        operator="Unit-Test",
        notes="Test note"
    )
    assert op_id is not None

    # Проверка получения по складу и дате (AP2)
    rows_wh = service.get_operations_by_warehouse_and_date(wh_test, today_str)
    found = any(r.operation_id == op_id for r in rows_wh)
    assert found, "Операция должна присутствовать в таблице operations_by_warehouse_date"

    # Проверка получения по товару (AP3)
    rows_item = service.get_operations_by_item(item_test)
    found_item = any(r.operation_id == op_id for r in rows_item)
    assert found_item, "Операция должна присутствовать в таблице operations_by_item"