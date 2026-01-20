from dotenv import load_dotenv
from playhouse.pool import PooledPsycopg3Database
import logging
import os

load_dotenv()

DB_NAME = os.environ.get('POSTGRES_DB', 'postgres')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', '')
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_PORT = os.environ.get('POSTGRES_PORT', '5432')

db = PooledPsycopg3Database(
  DB_NAME,
  user=DB_USER,
  password=DB_PASS,
  host=DB_HOST,
  port=DB_PORT,
  max_connections=25,
  stale_timeout=3600,
)

if os.environ.get('DEBUG') == 'True':
  logger = logging.getLogger('peewee')
  logger.setLevel(logging.DEBUG)
  logger.addHandler(logging.StreamHandler())

  db.logger = logger
  db.log_sql = True
