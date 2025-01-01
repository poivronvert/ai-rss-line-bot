#! /usr/local/env python3
import os
import sys
import logging

from my_journalist.utils.logger import setup_logging

import psycopg
from dotenv import load_dotenv

setup_logging()

logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_USER=os.environ["DATABASE_USER"]
DATABASE_PASSWORD=os.environ["DATABASE_PASSWORD"]
DATABASE_HOST=os.environ["DATABASE_HOST"]
DATABASE_PORT=os.environ["DATABASE_PORT"]
DATABASE_DB=os.environ["DATABASE_DB"]

sql = '''CREATE database line_chatbot_db'''

try:
    with psycopg.connect(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname="postgres"
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'line_chatbot_db'")
            if not cursor.fetchone():
                cursor.execute(sql)
                logger.info("✅Database 'line_chatbot_db' created successfully")
            else:
                logger.info("🟡 Database 'line_chatbot_db' already exists")
except Exception as e:
    logger.info(f"⛔️An error occurred: {e}")
    sys.exit(1)






