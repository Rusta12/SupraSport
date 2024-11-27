# Используем официальный образ Superset
FROM apache/superset:4.0.2

# Устанавливаем необходимые зависимости
USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    libpq-dev 

RUN pip install gunicorn gevent

# Копируем файл конфигурации в контейнер
COPY superset_config.py /app/pythonpath/
COPY logo-test.png /app/superset/static/assets/images/
COPY elogo.png /app/superset/static/assets/images/

# Переходим к пользователю superset
USER superset

#CMD ["superset", "run", "--host", "0.0.0.0", "--port", "8088"]
CMD ["gunicorn", "-w", "4", "-k", "gevent", "--timeout", "120", "-b", "0.0.0.0:8088", "superset.app:create_app()"]