import random
from datetime import datetime, timedelta
from .models import Movement

WAREHOUSES = ["WH-ALM", "WH-AST", "WH-SHM"]
PRODUCTS = ["P-1001", "P-1002", "P-1003", "P-1004", "P-1005", "P-1006"]
OPERATORS = ["op_anna", "op_boris", "op_chen", "op_dana"]


def generate(n: int = 60, seed: int = 42):
    """Синтетические движения: 5 суток на стыке месяцев (2026-09-28 .. 2026-10-02)."""
    rnd = random.Random(seed)
    start = datetime(2026, 9, 28, 8, 0, 0)
    out = []
    for i in range(n):
        ts = start + timedelta(days=rnd.randint(0, 4), minutes=rnd.randint(0, 600), seconds=i)
        out.append(Movement(
            warehouse_id=rnd.choice(WAREHOUSES),
            product_id=rnd.choice(PRODUCTS),
            movement_type=rnd.choice(["IN", "OUT", "OUT", "TRANSFER", "ADJUST"]),
            quantity=rnd.randint(1, 100),
            ts=ts,
            operator=rnd.choice(OPERATORS),
            doc_ref=f"DOC-{1000 + i}",
            comment="synthetic",
        ))
    return out
