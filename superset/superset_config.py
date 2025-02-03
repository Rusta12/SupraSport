import os

# Считывание переменных окружения из .env или Dockerfile
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'suprasport_db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')
SUPERSET_SECRET_KEY = os.getenv('SUPERSET_SECRET_KEY')

# Генерация безопасного SECRET_KEY
SECRET_KEY = SUPERSET_SECRET_KEY


# Настройка подключения к базе данных Superset
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Другие настройки Superset могут быть добавлены здесь

BABEL_DEFAULT_LOCALE = "ru"
LANGUAGES = {
    'en': {'flag': 'us', 'name': 'English'},
    'ru': {'flag': 'ru', 'name': 'Russian'},
}

FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "DRILL_BY": True,
    "DRILL_TO_DETAIL": True,
    "HORIZONTAL_FILTER_BAR": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "TAGGING_SYSTEM": True,
    "ENABLE_EXPLORE_DRAG_AND_DROP": True,
    "DASHBOARD_RBAC": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "ESCAPE_MARKDOWN_HTML": True,
    #"THUMBNAILS": True,
    "HORIZONTAL_FILTER_BAR": True,
}


D3_FORMAT = {
    "decimal": ",",
    "thousands": " ",
    "grouping": [3],
    "currency": ["", " руб."],
    "date": "%d.%m.%Y",
    "time": "%H:%M:%S",
}


#Без ограничения количества записей
#SQLLAB_CTAS_NO_LIMIT = True

APP_NAME = "Аналитика СУ"
APP_ICON="/static/assets/images/logo-test.png"
APP_ICON_WIDTH = 200
LOGO_TARGET_PATH = '/' 
LOGO_TOOLTIP = "Аналитика_Спорта"
FAVICONS = [{"href": "/static/assets/images/elogo.png"}]