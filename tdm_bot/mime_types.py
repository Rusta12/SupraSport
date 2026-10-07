"""Ворк-аунд для MIME-типов файловых вложений.

SDK (messenger_bot_api) вычисляет mimeType так:

    mimetypes.MimeTypes().guess_type(file_name)[0]

Свежий экземпляр MimeTypes() почти не содержит таблиц типов (на практике
2 записи — проверено и на Ubuntu-контейнере python:3.7, и локально),
поэтому для .xlsx/.docx/.csv он возвращает None, хотя модульная функция
mimetypes.guess_type() работает корректно. Платформа TDM отвечает
400 REQUIRED_FIELD_BLANK field=file.mimeType, а SDK глотает ошибку
и возбуждает FileUploadException: None — это и была причина падения
кнопки «Список организаций».

Решение не зависит от ОС: подменяем guess_type на уровне класса
MimeTypes — если таблицы не дали mime, используем фолбэк по расширению.
Применяется один раз при старте бота.
"""

import logging
import mimetypes
import os

logger = logging.getLogger(__name__)

EXTRA_MIME = {
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.xls': 'application/vnd.ms-excel',
    '.csv': 'text/csv',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.doc': 'application/msword',
    '.pdf': 'application/pdf',
}

_APPLIED = False

_ORIGINAL_GUESS = mimetypes.MimeTypes.guess_type


def _patched_guess(self, url, strict=True):
    guessed = _ORIGINAL_GUESS(self, url, strict)
    if guessed[0]:
        return guessed
    ext = os.path.splitext(str(url))[1].lower()
    fallback = EXTRA_MIME.get(ext)
    if fallback:
        return (fallback, guessed[1])
    return guessed


def apply_mime_workaround() -> None:
    """Однократная установка фолбэка. Идемпотентна, безопасно вызывать
    многократно (из menu_lists и из bot.py)."""
    global _APPLIED
    if _APPLIED:
        return
    mimetypes.MimeTypes.guess_type = _patched_guess
    _APPLIED = True
    logger.info('Применён MIME-ворк-аунд: фолбэк по расширению для вложений')