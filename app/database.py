import os
from contextlib import contextmanager
import mysql.connector
from dotenv import load_dotenv
from flask import current_app, has_app_context
load_dotenv()

def get_db_connection():
    testing = has_app_context() and current_app.config.get('TESTING', False)
    if testing:
        db_name = os.getenv('DB_TEST_NAME', 'risklens_test_db')
        if db_name != 'risklens_test_db':
            raise RuntimeError('Tests may connect only to risklens_test_db')
        if os.getenv('DB_NAME', 'risklens_db') == db_name:
            raise RuntimeError('Development and test databases must be different')
    else:
        db_name = os.getenv('DB_NAME', 'risklens_db')
    return mysql.connector.connect(host=os.getenv('DB_HOST','localhost'),
        user=os.getenv('DB_USER','root'), password=os.getenv('DB_PASSWORD',''),
        database=db_name, port=int(os.getenv('DB_PORT','3306')), autocommit=False)

@contextmanager
def db_transaction():
    conn = get_db_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        yield conn, cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        if cursor is not None: cursor.close()
        conn.close()
