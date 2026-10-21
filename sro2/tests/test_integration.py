"""Сценарии с живой Cassandra (docker compose up -d). Без БД пропускаются."""
import pytest
from datetime import datetime
from src.models import Movement

try:
    from src.db import connect, init_schema
    _cluster, _session = connect()
    init_schema(_session)
    AVAILABLE = True
except Exception:
    AVAILABLE = False

pytestmark = pytest.mark.skipif(not AVAILABLE, reason="Cassandra недоступна")


@pytest.fixture()
def repo():
    from src.repository import MovementRepository
    return MovementRepository(_session)


def _mv(ts, qty=3, t="IN"):
    return Movement("WH-TEST", "P-TEST", t, qty, ts, comment="t")


def test_create_goes_to_both_tables(repo):
    m = _mv(datetime(2026, 1, 5, 10))
    repo.add(m)
    assert any(r.movement_id == m.movement_id for r in repo.by_warehouse_day("WH-TEST", m.day))
    assert any(r.movement_id == m.movement_id for r in repo.by_product_month("P-TEST", m.year_month))
    repo.delete(m)


def test_clustering_order_desc(repo):
    a, b = _mv(datetime(2026, 2, 5, 9)), _mv(datetime(2026, 2, 5, 15))
    repo.add(a); repo.add(b)
    rows = repo.by_warehouse_day("WH-TEST", a.day)
    assert rows[0].ts > rows[-1].ts
    repo.delete(a); repo.delete(b)


def test_update_and_delete(repo):
    m = _mv(datetime(2026, 3, 5, 12))
    repo.add(m)
    repo.update_comment(m, "fixed")
    assert repo.by_warehouse_day("WH-TEST", m.day)[0].comment == "fixed"
    assert repo.by_product_month("P-TEST", m.year_month)[0].comment == "fixed"
    repo.delete(m)
    assert repo.by_warehouse_day("WH-TEST", m.day) == []
    assert repo.by_product_month("P-TEST", m.year_month) == []
