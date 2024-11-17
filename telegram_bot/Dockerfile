# Используем базовый образ с Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev 
    
# Копируем файлы requirements.txt и bot.py в контейнер
COPY ./ /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения
#ENV TELEGRAM_TOKEN=""
#ENV DB_HOST="db"
#ENV DB_NAME=""
#ENV DB_USER=""
#ENV DB_PASSWORD=""

# Запуск бота
CMD ["python", "bot.py"]