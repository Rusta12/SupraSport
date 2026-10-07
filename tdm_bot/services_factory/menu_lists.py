"""Сервисы кнопок главного меню: выгрузка списков в .xlsx.

Механика одинаковая для обеих кнопок:
  1. запрос из database.select_lists → pandas DataFrame;
  2. сериализация в Excel прямо в памяти (io.BytesIO) — без временных файлов;
  3. отправка вложением через SDK (File сам загрузит файл на fileupload).
pandas и openpyxl уже стоят в образе (Dockerfile).

Ошибки обработки не роняют бота: пользователь получает короткое
сообщение, а детали уходят в лог.
"""

import io
import logging
from datetime import date

from messenger_bot_api import MessageBotEvent, MessageRequest, File

from database.select_lists import (
    select_organizations_moskomport,
    select_organizations_other,
    select_federations,
)
from mime_types import apply_mime_workaround

# MIME-фолбэк для вложений: без него .xlsx уходит с mimeType=None,
# платформа отвечает 400 (REQUIRED_FIELD_BLANK file.mimeType).
# В bot.py тоже вызывается на старте — здесь страховка на ранний импорт.
apply_mime_workaround()

logger = logging.getLogger(__name__)


def _xlsx_file(df, base_name):
    """DataFrame → File с валидным .xlsx в памяти.

    :param base_name: начало имени файла без расширения, например
        'Список_организаций'; итог — 'Список_организаций_2026-10-05.xlsx'.
    """
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    filename = '{}_{}.xlsx'.format(base_name, date.today().isoformat())
    return File(filename, buffer.getvalue())


def _send_table(event: MessageBotEvent, df, base_name, intro):
    """Общий путь: dataframe → файл → ответ чату.

    Возвращает True при успехе. Пустой список и ошибки не роняют бота.
    """
    if df is None or df.shape[0] == 0:
        event.reply_text('По запросу ничего не нашлось — видимо, список пуст.')
        return False

    try:
        file = _xlsx_file(df, base_name)
        message = MessageRequest('{} (всего {} позиций).'.format(
            intro, df.shape[0]))
        event.reply_file_message(file, message)
        logger.info('Отправлен файл %s (%s строк)', file.name, df.shape[0])
        return True
    except Exception:
        logger.exception('Не удалось сформировать/отправить %s', base_name)
        event.reply_text('Не удалось сформировать файл. Попробуйте ещё раз.')
        return False


def send_organizations_msk_list(event: MessageBotEvent) -> bool:
    """Кнопка «Учреждения Москомспорта» → .xlsx"""
    logger.info('Запрошен список учреждений Москомспорта от %s', event.sender_id)
    try:
        df = select_organizations_moskomport()
    except Exception:
        logger.exception('Ошибка запроса списка учреждений Москомспорта')
        event.reply_text('Не удалось получить данные по учреждениям.')
        return False

    return _send_table(
        event, df, 'Учреждения_Москомспорта',
        'Учреждения в системе Москомспорта'
    )


def send_organizations_other_list(event: MessageBotEvent) -> bool:
    """Кнопка «Другие учреждения» → .xlsx"""
    logger.info('Запрошен список других учреждений от %s', event.sender_id)
    try:
        df = select_organizations_other()
    except Exception:
        logger.exception('Ошибка запроса списка других учреждений')
        event.reply_text('Не удалось получить данные по другим учреждениям.')
        return False

    return _send_table(
        event, df, 'Другие_учреждения',
        'Другие учреждения (с лицензией)'
    )


def send_federations_list(event: MessageBotEvent) -> bool:
    """Кнопка «Список Федераций» → .xlsx"""
    logger.info('Запрошен список федераций от %s', event.sender_id)
    try:
        df = select_federations()
    except Exception:
        logger.exception('Ошибка запроса списка федераций')
        event.reply_text('Не удалось получить данные по федерациям.')
        return False

    return _send_table(
        event, df, 'Список_федераций',
        'Актуальный список аккредитованных федераций'
    )