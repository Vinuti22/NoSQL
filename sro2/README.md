# SRO — вариант 15: История операций склада (Cassandra)

Дисциплина «Проектирование и применение NoSQL-технологий». Прототип хранения движений товаров по складу и дате
на Apache Cassandra: **две таблицы под разные Access Patterns** (по складу+дню и по товару+месяцу).

## Структура
```
README.md  requirements.txt  .env.example  docker-compose.yml
src/       models, db, repository (CRUD + запросы), seed_data
data/      schema.cql
scripts/   init_schema.py, seed.py, run_queries.py, draw_architecture.py
tests/     test_unit.py (без БД), test_integration.py (нужна Cassandra)
docs/      architecture.png, ADR.md, requirements.md, report.pdf, presentation.pdf
```

## Запуск
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                    # Windows: copy .env.example .env
docker compose up -d                                    # дождаться healthy (1-2 мин)
python scripts/init_schema.py                           # keyspace + 2 таблицы
python scripts/seed.py                                  # 60 синтетических движений
python scripts/run_queries.py                           # 8 демонстрационных запросов
pytest -v                                               # 3 unit + 3 integration сценария
```

## Модель данных
- `movements_by_warehouse_day`: PK `((warehouse_id, day), ts DESC, movement_id)` — AP1–AP4
- `movements_by_product`: PK `((product_id, year_month), ts DESC, movement_id)` — AP5–AP8

Подробнее: [ADR](docs/ADR.md), [требования и Access Patterns](docs/requirements.md), схема — `docs/architecture.png`.

## Материалы
- Отчёт: `docs/report.pdf` — _вставьте ссылку_
- Презентация: `docs/presentation.pdf` — _вставьте ссылку_
