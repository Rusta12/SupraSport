# Используем официальный образ Superset
FROM apache/superset:4.0.2

# Устанавливаем необходимые зависимости
USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    libpq-dev 

# Копируем файл конфигурации в контейнер
COPY superset_config.py /app/pythonpath/
COPY logo-test.png /app/superset/static/assets/images/

# Переходим к пользователю superset
USER superset

# Инициализация базы данных Superset
#RUN superset db upgrade

# Создание административного пользователя
#RUN superset fab create-admin \
#    --username admin \
#    --firstname Admin \
#    --lastname User \
#    --email admin@admin.com \
#    --password admin

# Загрузка примеров данных
#RUN superset load_examples

# Сборка статических файлов
#RUN superset init

# Открываем порт для доступа к Superset
#EXPOSE 8088
# Сборка статических файлов и подготовка Superset
#RUN superset init

# Команда для запуска Superset
CMD ["superset", "run", "--host", "0.0.0.0", "--port", "8088"]
