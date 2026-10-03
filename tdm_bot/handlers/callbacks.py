import re
# Модули
from services_factory.services_sport import print_sport, print_school

def mean_allocation(event, data: str):
    """Функция распределения по обработчикам на основе callback_data"""
    patern_gos = r'gos_'
    gos = re.match(patern_gos, data)

    patern_sport = r'sport_menu_'
    sport = re.match(patern_sport, data)

    patern_school = r'sсhool_menu_'
    school = re.match(patern_school, data)

    patern_fed = r'fed_'
    fed = re.match(patern_fed, data)

    if data == 'gos_menu':
        #from gosorder.menu_gos_inline import gos_menu_general
        return #gos_menu_general(event)
        
    if data == 'fed_menu':
        #from fedorder.menu_fed_inline import fed_menu_general
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
        event.reply_text(f'Команда не распознана: {data}')
