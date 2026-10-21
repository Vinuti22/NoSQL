"""8 демонстрационных запросов (2 нетривиальных). Запуск: python scripts/run_queries.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from datetime import date, datetime
from src.db import connect, init_schema
from src.repository import MovementRepository

cluster, session = connect()
init_schema(session)
repo = MovementRepository(session)
WH, P, D = "WH-ALM", "P-1001", date(2026, 10, 1)


def show(title, rows):
    print(f"\n== {title} ==")
    for r in rows[:5]:
        print(" ", r)
    print(f"  (строк: {len(rows)})")


show("Q1 AP1: все операции склада за день", repo.by_warehouse_day(WH, D))
show("Q2 AP2: последние 5 операций склада за день", repo.last_by_warehouse_day(WH, D, 5))
show("Q3 AP3: операции склада за интервал 08:00-12:00",
     repo.by_warehouse_range(WH, D, datetime(2026, 10, 1, 8), datetime(2026, 10, 1, 12)))
print("\n== Q4 AP4 (нетривиальный): итоги по типам за день ==", repo.daily_totals(WH, D))
show("Q5 AP5: история товара за месяц", repo.by_product_month(P, "2026-10"))
show("Q6 AP6: последние 5 движений товара", repo.last_by_product(P, "2026-10", 5))
show("Q7 AP7: движения товара за интервал",
     repo.by_product_range(P, "2026-10", datetime(2026, 10, 1), datetime(2026, 10, 3)))
print("\n== Q8 AP8 (нетривиальный): оборот товара по месяцам ==",
      repo.product_turnover(P, ["2026-09", "2026-10"]))
cluster.shutdown()
