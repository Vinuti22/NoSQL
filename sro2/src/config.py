import os
from dotenv import load_dotenv

load_dotenv()

HOSTS = [h.strip() for h in os.getenv("CASSANDRA_HOSTS", "127.0.0.1").split(",")]
PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "warehouse")
USERNAME = os.getenv("CASSANDRA_USERNAME") or None
PASSWORD = os.getenv("CASSANDRA_PASSWORD") or None
