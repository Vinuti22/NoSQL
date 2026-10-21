"""Сценарии без БД: бакетирование, валидация, генератор данных."""
import pytest
from datetime import datetime
from src.models import Movement, month_bucket
from src.seed_data import generate


def test_month_bucket_and_day():
    m = Movement("WH-1", "P-1", "IN", 5, datetime(2026, 9, 30, 23, 59))
    assert m.year_month == "2026-09" and str(m.day) == "2026-09-30"
    assert month_bucket(datetime(2026, 10, 1)) == "2026-10"


def test_validation():
    with pytest.raises(ValueError):
        Movement("WH-1", "P-1", "BAD", 5, datetime.now())
    with pytest.raises(ValueError):
        Movement("WH-1", "P-1", "IN", 0, datetime.now())


def test_seed_generator_size_and_two_buckets():
    rows = generate(60)
    assert len(rows) >= 30
    assert len({r.year_month for r in rows}) == 2  # стык месяцев демонстрирует bucketing
