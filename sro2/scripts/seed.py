import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from src.db import connect, init_schema
from src.repository import MovementRepository
from src.seed_data import generate

cluster, session = connect()
init_schema(session)
repo = MovementRepository(session)
rows = generate(60)
for m in rows:
    repo.add(m)
print(f"Загружено движений: {len(rows)} (в обе таблицы)")
cluster.shutdown()
