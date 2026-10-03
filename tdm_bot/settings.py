import os

# Считывание переменных окружения
DB_PROD_HOST = os.getenv('DB_HOST', 'suprasport_db')
DB_PROD_DATABASE = os.getenv('DB_NAME')
DB_PROD_NAME = os.getenv('DB_USER')
DB_PROD_PASSWORD = os.getenv('DB_PASSWORD')

# Токен и URL для мессенджера tdm.mos.ru
TOKEN = os.getenv('MESSENGER_TOKEN')
REST = os.getenv('MESSENGER_REST')
SSE = os.getenv('MESSENGER_SSE')
FILE = os.getenv('MESSENGER_FILE')
