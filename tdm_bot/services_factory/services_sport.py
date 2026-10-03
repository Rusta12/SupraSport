from messenger_bot_api import MessageBotEvent
# Модули
from services_factory.factory_info_sport import sport_mean_reg
from services_factory.factory_info_school import school_mean_reg

def print_sport(event: MessageBotEvent, data: str):
    """Вывод информации по виду спорта"""
    #from original_request.sport_menu.kpi_sport_menu import get_sport_kpi
    try:
        result = sport_mean_reg(data)
        event.reply_text(result)
    except Exception as e:
        event.reply_text('Ошибка при получении данных')
        print(f'ОШИБКА {e}')


def print_school(event: MessageBotEvent, data: str):
    """Вывод информации по виду спорта"""
    #from original_request.sport_menu.kpi_sport_menu import get_sport_kpi
    try:
        result = school_mean_reg(data)
        event.reply_text(result)
    except Exception as e:
        event.reply_text('Ошибка при получении данных')
        print(f'ОШИБКА {e}')
