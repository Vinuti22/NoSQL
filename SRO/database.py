import os
from cassandra.cluster import Cluster
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            nodes = os.getenv("CASSANDRA_NODES", "127.0.0.1").split(",")
            port = int(os.getenv("CASSANDRA_PORT", 9042))
            cls._instance.cluster = Cluster(nodes, port=port)
            cls._instance.session = cls._instance.cluster.connect()
        return cls._instance

    @classmethod
    def get_session(cls):
        if cls._instance is None:
            cls()
        return cls._instance.session

    @classmethod
    def close(cls):
        if cls._instance and cls._instance.cluster:
            cls._instance.cluster.shutdown()
            cls._instance._instance = None