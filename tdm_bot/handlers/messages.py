import logging

import pandas as pd

from messenger_bot_api import MessageBotEvent, MessageRequest
# Модули
from bot_documents.default_text import ekp_text, ias_text, minsport_text
from database.select_ref import sport_token
from database.insert_log import (
    log_input,
    log_denied,
    CATEGORY_SPORT,
    CATEGORY_INFO,
    RESULT_OK,
    RESULT_NOT_FOUND,
    RESULT_MANY_OPTIONS,
    RESULT_TOO_MANY
)
from handlers.data_classs import SportClass
from handlers.callinline_button import output_inline_sport
from handlers.callbacks import mean_allocation
from protection.check_prot import validation_user, access_denied_text

logger = logging.getLogger(__name__)

# Справочные тексты без спортивных данных
INFO_KEYWORDS = {
    'справка': ['екп', 'календарь', 'кп', 'мероприятия'],
    'справка_ias': ['иас'],
    'справка_fed': ['емир', 'минспорт', 'гис', 'фгис', 'министерство'],
}

# Больше этого числа вариантов не показываем — пользователю нужен
# более узкий запрос, а не список из сотни позиций
MAX_INLINE_OPTIONS = 15


def receiving_messages(text: str) -> pd.DataFrame:
    """Поиск по тексту в справочнике меню"""
    text = text.lower()
    df = sport_token()
    df_sersh = df[(df['token_name'].str.contains(fr"{text}", na=False))]
    df_sersh = df_sersh[['menu', 'correct_name']]
    # Присваиваем копию: drop_duplicates(inplace=True) на срезе
    # выдаёт SettingWithCopyWarning и может не примениться
    df_sersh = df_sersh.drop_duplicates().reset_index(drop=True)
    return df_sersh


def assemble_message(event: MessageBotEvent):
    """Основной алгоритм обработки текстовых сообщений"""
    text = event.message_text
    if text is None:
        return

    # Логируем ДО проверки прав: интересно, что человек пытался запросить,
    # даже если не получил
    if validation_user(event, 1) is not True:
        logger.info('Нет доступа к разделу для %s', event.sender_id)
        log_denied(event, message_text=text)
        event.reply_text(access_denied_text(1))
        return

    text_lower = text.lower().strip()

    if text_lower in INFO_KEYWORDS['справка']:
        log_input(event, text, result=RESULT_OK, category=CATEGORY_INFO,
                  menu_function='info_ekp')
        return ekp_text(event)
    elif text_lower in INFO_KEYWORDS['справка_ias']:
        log_input(event, text, result=RESULT_OK, category=CATEGORY_INFO,
                  menu_function='info_ias')
        return ias_text(event)
    elif text_lower in INFO_KEYWORDS['справка_fed']:
        log_input(event, text, result=RESULT_OK, category=CATEGORY_INFO,
                  menu_function='info_fed')
        return minsport_text(event)

    df = receiving_messages(text)

    if df.shape[0] == 0:
        log_input(event, text, result=RESULT_NOT_FOUND, category=CATEGORY_SPORT)
        event.reply_text(
            '🚴‍♂️ По вашему запросу ничего не найдено. '
            'Попробуйте уточнить запрос.'
        )
        return

    if df.shape[0] > MAX_INLINE_OPTIONS:
        log_input(event, text, result=RESULT_TOO_MANY,
                  result_count=df.shape[0], category=CATEGORY_SPORT)
        event.reply_text(
            'Ваш запрос содержит большое количество вариантов, '
            'пожалуйста дайте мне оптимальный контекст.'
        )
        return

    if df.shape[0] == 1:
        # Пользователь сразу попал в нужный раздел — запрос завершён
        menu = df.loc[0, 'menu']
        log_input(event, text, result=RESULT_OK, category=CATEGORY_SPORT,
                  menu_function=menu, finish_check=True)
        return mean_allocation(event, menu)

    # Несколько вариантов — показываем кнопки, решение пользователь примет позже
    log_input(event, text, result=RESULT_MANY_OPTIONS, result_count=df.shape[0],
              category=CATEGORY_SPORT)
    input_class = SportClass(
        id_user=event.sender_id,
        df=df,
        text_user=text
    )
    return output_inline_sport(event, input_class)