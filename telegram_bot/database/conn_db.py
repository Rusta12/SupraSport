import psycopg2
import psycopg2.extras as extras
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
import os
import sys
import settings


param_dic = {
    "host"      : settings.DB_PROD_HOST,
    "database"  : settings.DB_PROD_DATABASE,
    "user"      : settings.DB_PROD_NAME,
    "password"  : settings.DB_PROD_PASSWORD,
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 5,
    "options": "-c search_path=supra",
}


# Функция конекта
def connect(params_dic):
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn
    
conn = connect(param_dic)

# Функция запроса к БД для получения DataFrame
def postgresql_to_dataframe(select_query, column_names):
    """
    Преобразование SELECT запроса
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    # Получаем список кортежей
    tupples = cursor.fetchall()
    cursor.close()
    # Список отдаем в пандас
    df = pd.DataFrame(tupples, columns=column_names)
    return df

# Функция отправки DataFrame в БД по имени столбцам
def copy_from_file(df, table, col_bd):
    tmp_df = "./tmp_dataframe.csv"
    df.to_csv(tmp_df, index=False, header=False, sep='\t')
    f = open(tmp_df, 'r')
    cursor = conn.cursor()
    try:
        cursor.copy_from(f, table, sep="\t",
                         columns=col_bd)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        f.close()
        os.remove(tmp_df)
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("Export file done")
    cursor.close()
    f.close()
    os.remove(tmp_df)

# Функция отправки DataFrame данных в БД
def copy_from_all(df, table):
    tmp_df = "./tmp_dataframe.csv"
    df.to_csv(tmp_df, index=False, header=False, sep='\t')
    f = open(tmp_df, 'r')
    cursor = conn.cursor()
    try:
        cursor.copy_from(f, table, sep="\t")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        f.close()
        os.remove(tmp_df)
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("Export file done")
    cursor.close()
    f.close()
    os.remove(tmp_df)
 

# Функция не изменяемого списка
def postgresql_to_check(select_query):
    """
    Преобразование SELECT запроса
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    # Получаем список кортежей
    tupples = cursor.fetchone()
    cursor.close()
    # Список отдаем
    return tupples[0]


# Функция не изменяемого списка
def postgresql_to_tables(select_query):
    """
    Преобразование SELECT запроса
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    tables = cursor.fetchall()
    cursor.close()
    # Список отдаем
    return tables
    
# Функция insert, update, delete
def postgresql_to_data(select_query):
    """
    Преобразование SELECT запроса
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    # сохраняем данны
    cursor.close()
    #print('Данные успешно обновились/добавились')
