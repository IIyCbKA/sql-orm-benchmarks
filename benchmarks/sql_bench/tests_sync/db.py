from contextlib import contextmanager
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT")

CONNINFO = (
    f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} "
    f"host={DB_HOST} port={DB_PORT}"
)

@contextmanager
def get_connection():
    conn = psycopg.connect(CONNINFO, autocommit=True, prepare_threshold=0)
    try:
        yield conn
    finally:
        conn.close()
