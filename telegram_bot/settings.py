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


# Настройки MTPROTO прокси
PROXY_TYPE = 'socks5'  # или 'socks5h' (если нужно резолвить домены через прокси)
PROXY_ADDR = "141.98.189.185"  # IP прокси сервера
PROXY_PORT = 443  # Порт (обычно 1080, 443 или 80)
PROXY_SECRET = "ee1c677bc896a228c1e4d31b536ab8199b706574726f766963682e7275"  # Secret от MTPROTO