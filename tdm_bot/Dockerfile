FROM python:3.7

# Устанавливаем libGL.so.1 через apt (нужна для cv2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем файлы зависимостей
#COPY tdm_bot/requirements.txt /app/requirements.txt
COPY tdm_bot/messenger_bot_api-2.0.5-py3-none-any.whl /app/messenger_bot_api-2.0.5-py3-none-any.whl

# Устанавливаем зависимости
#RUN pip install --no-cache-dir /app/messenger_bot_api-2.0.5-py3-none-any.whl &&\
#    pip install --no-cache-dir -r /app/requirements.txt 
# Так почему то зависимости не могут установится по этому используем способ ниже

RUN pip install --no-cache-dir \
        click \
        jmespath \
        requests \
        sseclient-py \
        psycopg2-binary==2.9.9 \
        pandas==1.3.5 \
        openpyxl==3.0.10 \
        xlrd==2.0.1 \
        numpy==1.21.6 && \
    pip install --no-cache-dir /app/messenger_bot_api-2.0.5-py3-none-any.whl

# Копируем код бота
COPY tdm_bot/ /app/

# Создаём временные директории
RUN mkdir -p /app/gosorder/update_gosorder/Temp \
             /app/gosorder/reporter_gosorder/Temp \
             /app/fedorder/Temp

CMD ["python", "bot.py"]
