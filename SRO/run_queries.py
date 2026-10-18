from datetime import datetime
from src.database import DatabaseConnection
from src.models import WarehouseOperationService

def run_demos():
    service = WarehouseOperationService()
    today_str = datetime.now().strftime("%Y-%m-%d")
    wh_id = "WH-Almaty-01"
    item_id = "ITEM-9901"

    print("=== ДЕМОНСТРАЦИЯ 8 ЗАПРОСОВ ===")

    # 1. Запрос 1: История операций по складу и дате (AP2)
    print(f"\n[Запрос 1] История склада {wh_id} за {today_str}:")
    rows1 = service.get_operations_by_warehouse_and_date(wh_id, today_str)
    for r in rows1[:3]:
        print(f" - Время: {r.operation_time}, Товар: {r.item_id}, Тип: {r.operation_type}, Кол-во: {r.quantity}")

    # 2. Запрос 2: История движения конкретного товара (AP3)
    print(f"\n[Запрос 2] История движения товара {item_id}:")
    rows2 = service.get_operations_by_item(item_id)
    for r in rows2[:3]:
        print(f" - Склад: {r.warehouse_id}, Время: {r.operation_time}, Тип: {r.operation_type}, Кол-во: {r.quantity}")

    # 3. Запрос 3: Фильтрация по типу операции ('IN') (AP4)
    print(f"\n[Запрос 3] Операции прихода (IN) по складу {wh_id}:")
    rows3 = service.get_operations_by_type(wh_id, today_str, 'IN')
    for r in rows3[:3]:
        print(f" - {r.operation_time} | Товар: {r.item_id} | +{r.quantity} шт.")

    # 4. Запрос 4: Получение последних 3 операций (лимит) (AP5)
    print(f"\n[Запрос 4] Последние 3 операции по складу {wh_id}:")
    rows4 = service.get_latest_operations(wh_id, today_str, limit=3)
    for r in rows4:
        print(f" - {r.operation_time} | {r.operation_type} | {r.item_id} | {r.quantity} шт.")

    # 5. Запрос 5: Фильтрация по временному диапазону (AP6)
    print(f"\n[Запрос 5] Операции за последний час:")
    now = datetime.now()
    start_t = now.replace(hour=0, minute=0, second=0)
    end_t = now
    rows5 = service.get_operations_by_time_range(wh_id, today_str, start_t, end_t)
    print(f" Найдено операций в диапазоне: {len(rows5)}")

    # 6. Запрос 6 (Нетривиальный): Аналитический срез баланса (оборот) (AP8)
    print(f"\n[Запрос 6 - Нетривиальный] Баланс оборота товаров по складу {wh_id}:")
    turnover = service.get_daily_turnover_analytics(wh_id, today_str)
    for itm, balance in turnover.items():
        print(f" - Товар {itm}: чистый баланс = {balance:+d} шт.")

    # 7. Запрос 7 (Нетривиальный): Обновление примечания к операции (AP7)
    print(f"\n[Запрос 7 - Нетривиальный] Обновление примечания (UPDATE):")
    if rows1:
        target = rows1[0]
        service.update_operation_notes(wh_id, today_str, target.operation_time, target.operation_id, "Проверено аудитором")
        print(f" - Успешно обновлено примечание для операции {target.operation_id}")

    # 8. Запрос 8: Проверка вставки новой операции (AP1)
    print(f"\n[Запрос 8] Вставка новой тестовой операции (INSERT):")
    new_id = service.record_operation(wh_id, "ITEM-9904", "OUT", 12, "Оператор Тест", "Ручная отгрузка")
    print(f" - Успешно создана операция с timeuuid: {new_id}")

    DatabaseConnection.close()

if __name__ == "__main__":
    run_demos()