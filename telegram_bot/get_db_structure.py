import json
from database.conn_db import postgresql_to_tables
from datetime import datetime

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Преобразование в строку
    raise TypeError("Type not serializable")


def get_db_structure_with_data():
    try:
        db_structure = {"tables": {}}

        # Получаем список таблиц
        tables = postgresql_to_tables("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)

        for table in tables:
            table_name = table[0]
            db_structure["tables"][table_name] = {
                "columns": {}, 
                "foreign_keys": {},
                "sample_data": []  # для хранения примеров данных
            }

            # Получаем информацию о колонках
            columns = postgresql_to_tables(f"""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}';
            """)
            for column in columns:
                column_name, data_type, is_nullable = column
                db_structure["tables"][table_name]["columns"][column_name] = {
                    "type": data_type,
                    "nullable": is_nullable == 'YES'
                }

            # Получаем информацию о внешних ключах
            foreign_keys = postgresql_to_tables(f"""
                SELECT 
                    kcu.column_name, 
                    ccu.table_name AS foreign_table, 
                    ccu.column_name AS foreign_column 
                FROM 
                    information_schema.key_column_usage AS kcu
                JOIN 
                    information_schema.constraint_column_usage AS ccu 
                    ON kcu.constraint_name = ccu.constraint_name
                JOIN 
                    information_schema.table_constraints AS tc
                    ON tc.constraint_name = kcu.constraint_name
                WHERE 
                    tc.constraint_type = 'FOREIGN KEY' AND kcu.table_name = '{table_name}';
            """)
            for fk in foreign_keys:
                column_name, foreign_table, foreign_column = fk
                db_structure["tables"][table_name]["foreign_keys"][column_name] = {
                    "references_table": foreign_table,
                    "references_column": foreign_column
                }

            # Получаем пример данных
            sample_data = postgresql_to_tables(f"SELECT * FROM {table_name} LIMIT 5;")
            db_structure["tables"][table_name]["sample_data"] = sample_data

        return json.dumps(db_structure, indent=4, default=str)  # default=str для корректной обработки типов данных

    except Exception as e:
        print("Error:", e)

