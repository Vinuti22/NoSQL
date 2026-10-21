import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from src.db import connect, init_schema

cluster, session = connect()
init_schema(session)
print("Схема создана.")
cluster.shutdown()
