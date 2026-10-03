import psycopg2
import pandas as pd
from io import StringIO
import settings


def get_connection():
    """Создание подключения к PostgreSQL"""
    conn = psycopg2.connect(
        host=settings.DB_PROD_HOST,
        database=settings.DB_PROD_DATABASE,
        user=settings.DB_PROD_NAME,
        password=settings.DB_PROD_PASSWORD
    )
    return conn


def postgresql_to_dataframe(query: str, column_names: list) -> pd.DataFrame:
    """Выполнение SELECT запроса и возврат DataFrame"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=column_names)
        return df
    finally:
        cursor.close()
        conn.close()
