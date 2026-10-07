"""Проверка уровня доступа.

Роль «без доступа» в системе отсутствует: 1 «Аналитик» открывает весь текущий
функционал, 2 «Старший аналитик» зарезервирован под закрытую информацию.
Поэтому проверка уровня 1 на текущем этапе никого не отсекает — это ожидаемое
поведение, а не ошибка. Реальные ограничения появятся вместе с закрытым
контентом для роли 2.
"""

import logging

from protection.protection_insert import get_user_access, is_archived
from protection.roles import ROLE_ANALYTIC, role_name

logger = logging.getLogger(__name__)

DENIED_TEXT = 'У вас недостаточно уровня доступа к этому разделу.'


def access_denied_text(required_role=None) -> str:
    """Текст отказа. required_role=None — админская команда (нужна роль 2)."""
    if required_role is None:
        return 'Команда доступна только администраторам.'
    return 'Раздел доступен только роли «{}».\n{}'.format(
        role_name(required_role), DENIED_TEXT
    )


def validation_user(event, lvl: int) -> bool:
    """Проверка доступа для текущего события.

    Архивные пользователи (arhiv = true) не проходят проверку ни при какой
    роли — покинувший чат человек не должен продолжать работать с ботом.
    """
    user_id = getattr(event, 'sender_id', None)
    if user_id is None:
        return False

    if is_archived(user_id):
        logger.info('Отказ: пользователь %s архивный', user_id)
        return False

    access = get_user_access(user_id)
    return access >= lvl


def validation_user_other(user_id, lvl: int) -> bool:
    """Проверка доступа вне события — без отправки сообщений пользователю"""
    if is_archived(user_id):
        return False
    return get_user_access(user_id) >= lvl


def is_senior(event) -> bool:
    """Является ли отправитель Старшим аналитиком"""
    return validation_user(event, 2)


def is_admin(event) -> bool:
    """Админские команды (реестр чатов и т.п.) — только Старший аналитик"""
    return validation_user(event, 2)


__all__ = [
    'DENIED_TEXT',
    'ROLE_ANALYTIC',
    'access_denied_text',
    'validation_user',
    'validation_user_other',
    'is_senior',
    'is_admin',
]