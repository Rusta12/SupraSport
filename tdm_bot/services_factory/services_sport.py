import logging

from messenger_bot_api import MessageBotEvent
# Модули
from services_factory.factory_info_sport import sport_mean_reg
from services_factory.factory_info_school import school_mean_reg
from database.insert_log import (
    log_input,
    CATEGORY_SPORT,
    RESULT_OK,
    RESULT_ERROR
)

logger = logging.getLogger(__name__)


def print_sport(event: MessageBotEvent, data: str):
    """Вывод информации по виду спорта"""
    try:
        result = sport_mean_reg(data)
        event.reply_text(result)
        # Пользователь дошёл до ответа по конкретному виду спорта
        log_input(event, message_text=None, menu_function=data,
                  result=RESULT_OK, category=CATEGORY_SPORT, finish_check=True)
    except Exception as e:
        logger.exception('Ошибка получения данных по виду спорта %r', data)
        event.reply_text('Ошибка при получении данных')
        log_input(event, message_text=None, menu_function=data,
                  result=RESULT_ERROR, category=CATEGORY_SPORT)


def print_school(event: MessageBotEvent, data: str):
    """Вывод информации по учебному учреждению"""
    try:
        result = school_mean_reg(data)
        event.reply_text(result)
        log_input(event, message_text=None, menu_function=data,
                  result=RESULT_OK, category=CATEGORY_SPORT, finish_check=True)
    except Exception as e:
        logger.exception('Ошибка получения данных по учреждению %r', data)
        event.reply_text('Ошибка при получении данных')
        log_input(event, message_text=None, menu_function=data,
                  result=RESULT_ERROR, category=CATEGORY_SPORT)