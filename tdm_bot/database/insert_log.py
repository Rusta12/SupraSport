"""Журнал обращений пользователей.

Отвечает на два вопроса аналитики:
  * message_text  — ЧТО пользователь вводил;
  * menu_function / callback_data / category — ЧЕМ пользовался.

Принципы:
  1. Ошибка записи в журнал НЕ должна ронять обработку сообщения —
     пользователь спросил про спорт, а не про нашу базу.
  2. Не оборачиваем в транзакции вместе с бизнес-логикой: каждый вызов
     коммитит сразу, иначе ответ пользователю будет ждать запись в лог.
  3. Логируем ДО проверки прав, с result='denied' — интересно, что человек
     пытался запросить, даже если не получил.
"""

import logging

from database.conn_db import postgresql_to_data
from protection.protection_insert import to_user_id

logger = logging.getLogger(__name__)

# Значения колонки result
RESULT_OK = 'ok'
RESULT_NOT_FOUND = 'not_found'
RESULT_MANY_OPTIONS = 'many_options'
RESULT_TOO_MANY = 'too_many'
RESULT_ERROR = 'error'
RESULT_DENIED = 'denied'

# Группы функционала (колонка category)
CATEGORY_SPORT = 'спорт'
CATEGORY_INFO = 'справка'
CATEGORY_SERVICE = 'сервис'

# Длинный текст без смысла хранить целиком: пользователь может вставить
# простыню, и таблица разрастётся.
MAX_TEXT_LENGTH = 500


def truncate_text(text) -> str:
    """Обрезка текста запроса с записью об усечении"""
    if text is None:
        return None
    text = str(text)
    if len(text) > MAX_TEXT_LENGTH:
        return text[:MAX_TEXT_LENGTH]
    return text


def insert_log(event, message_text=None, category=None, menu_function=None,
               callback_data=None, command=None, result=RESULT_OK,
               result_count=None, finish_check=False) -> bool:
    """Запись одного обращения в tdm_bot.user_log_analize.

    Никогда не бросает исключений: любая ошибка уходит в лог и возвращает
    False, чтобы вызывающий код продолжил работу.
    """
    try:
        user_id = to_user_id(getattr(event, 'sender_id', None))
        if user_id is None:
            logger.debug('Событие без sender_id — журнал пропущен')
            return False

        workspace_id = getattr(event, 'workspace_id', None)
        group_id = getattr(event, 'group_id', None)

        # Итоговое описание раздела: если явный menu_function не задан,
        # для команд используем команду, для кнопок — callback_data.
        menu = menu_function
        if menu is None:
            menu = command or callback_data

        postgresql_to_data(
            """
            INSERT INTO user_log_analize
                (id_user, workspace_id, group_id, message_text, command,
                 menu_function, callback_data, category, result,
                 result_count, finish_check)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (user_id,
             workspace_id,
             group_id,
             truncate_text(message_text),
             truncate_text(command),
             truncate_text(menu),
             truncate_text(callback_data),
             truncate_text(category),
             truncate_text(result),
             result_count,
             bool(finish_check))
        )
        return True
    except Exception:
        logger.exception('Не удалось записать журнал обращения '
                         '(это не должно ломать ответ пользователю)')
        return False


def log_command(event, command: str, result=RESULT_OK, category=CATEGORY_SERVICE):
    """Журнал для команд /start, /profile"""
    return insert_log(event, message_text=command, command=command,
                      category=category, result=result)


def log_button(event, callback_data: str, menu_function=None,
               result=RESULT_OK, category=CATEGORY_SPORT):
    """Журнал для нажатия inline-кнопки"""
    return insert_log(event, message_text=None, category=category,
                      menu_function=menu_function,
                      callback_data=callback_data, result=result)


def log_input(event, message_text: str, result=RESULT_OK,
              result_count=None, category=None, menu_function=None,
              finish_check=False):
    """Журнал для введённого текста — главный источник «что вводили»"""
    return insert_log(event, message_text=message_text, category=category,
                      menu_function=menu_function, result=result,
                      result_count=result_count, finish_check=finish_check)


def log_denied(event, message_text=None, menu_function=None):
    """Отказ по правам"""
    return insert_log(event, message_text=message_text, category=CATEGORY_SERVICE,
                      menu_function=menu_function, result=RESULT_DENIED)