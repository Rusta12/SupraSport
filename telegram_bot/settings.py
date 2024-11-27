import os

# Считывание переменных окружения из .env или Dockerfile
DB_PROD_HOST = os.getenv('DB_HOST', 'suprasport_db')
DB_PROD_DATABASE = os.getenv('DB_NAME')
DB_PROD_NAME = os.getenv('DB_USER')
DB_PROD_PASSWORD = os.getenv('DB_PASSWORD')

TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI = os.getenv('OPENAI_API_KEY')

CATALOG_ID = os.getenv('CATALOG_ID')
Y_Api_Key = os.getenv('Y_Api_Key')


