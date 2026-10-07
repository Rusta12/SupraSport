import logging

import psycopg2
import pandas as pd
import settings

logger = logging.getLogger(__name__)

# Схема с данными бота TDM. Ставится в search_path, поэтому новый код
# обращается к таблицам без префикса: FROM user_protection.
# Legacy-схему supra код не трогает — все её запросы квалифицированы явно.
TDM_SCHEMA = 'tdm_bot'
SEARCH_PATH = '{schema},public'.format(schema=TDM_SCHEMA)


def get_connection():
    """Создание подключения к PostgreSQL"""
    conn = psycopg2.connect(
        host=settings.DB_PROD_HOST,
        database=settings.DB_PROD_DATABASE,
        user=settings.DB_PROD_NAME,
        password=settings.DB_PROD_PASSWORD,
        options='-c search_path={}'.format(SEARCH_PATH)
    )
    return conn


def postgresql_to_dataframe(query: str, column_names: list) -> pd.DataFrame:
    """Выполнение SELECT запроса и возврат DataFrame"""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=column_names)
        return df
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def postgresql_to_dataframe_params(query: str, column_names: list, params: tuple) -> pd.DataFrame:
    """SELECT с параметрами. Параметры передаются отдельно от текста запроса —
    это единственно допустимый способ подставлять значения, строковая
    склейка в стиле Telegram-версии не используется."""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=column_names)
        return df
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def postgresql_to_data(query: str, params: tuple) -> None:
    """Выполнение INSERT/UPDATE/DELETE с последующим commit"""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def postgresql_to_check(query: str, params: tuple):
    """Скалярный SELECT — возвращает первое значение первой строки"""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()