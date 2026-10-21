from pathlib import Path
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from . import config

SCHEMA = Path(__file__).resolve().parent.parent / "data" / "schema.cql"


def connect():
    auth = None
    if config.USERNAME:
        auth = PlainTextAuthProvider(config.USERNAME, config.PASSWORD)
    cluster = Cluster(config.HOSTS, port=config.PORT, auth_provider=auth)
    return cluster, cluster.connect()


def init_schema(session):
    text = SCHEMA.read_text(encoding="utf-8")
    lines = [l for l in text.splitlines() if not l.strip().startswith("--")]
    for stmt in "\n".join(lines).split(";"):
        if stmt.strip():
            session.execute(stmt)
    session.set_keyspace(config.KEYSPACE)
