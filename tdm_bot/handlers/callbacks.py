import logging
import re
# Модули
from services_factory.services_sport import print_sport, print_school
from services_factory.menu_lists import (
    send_organizations_msk_list,
    send_organizations_other_list,
    send_federations_list,
)

logger = logging.getLogger(__name__)


def mean_allocation(event, data: str):
    """Функция распределения по обработчикам на основе callback_data"""
    patern_gos = r'gos_'
    gos = re.match(patern_gos, data)

    patern_sport = r'sport_menu_'
    sport = re.match(patern_sport, data)

    # В справочнике префикс записан как 'sсhool_menu_', где второй символ —
    # КИРИЛЛИЧЕСКАЯ с (U+0441, ascii 1089), а не латинская c (ascii 108).
    # Это опечатка при вводе данных: проверено в БД, ascii(2-й символ)=1089.
    # Принимаем оба написания — и текущие данные, и исправленные в справочнике.
    # Раньше здесь стояла только кириллическая с; замена на латинскую,
    # наоборот, ломала маршрутизацию.
    school = re.match(r's[сc]hool_menu_', data)

    patern_fed = r'fed_'
    fed = re.match(patern_fed, data)

    # Кнопки главного меню (menu_mean) — выгрузки-списки
    if data == 'list_org_moskomport':
        return send_organizations_msk_list(event)
    if data == 'list_org_other':
        return send_organizations_other_list(event)
    if data == 'list_federations':
        return send_federations_list(event)

    if data == 'gos_menu':
        #from gosorder.menu_gos_inline import gos_menu_general
        logger.info('Раздел ГОС задание пока не реализован')
        return #gos_menu_general(event)

    if data == 'fed_menu':
        #from fedorder.menu_fed_inline import fed_menu_general
        logger.info('Раздел Федерации пока не реализован')
        return #fed_menu_general(event)

    if gos:
        return #gos_reception(event, data)
    elif sport:
        return print_sport(event, data)
    elif school:
        return print_school(event, data)
    elif fed:
        return #fed_reception(event, data)
    else:
        logger.warning('Нераспознанный callback_data: %r', data)
        event.reply_text(f'Команда не распознана: {data}')
