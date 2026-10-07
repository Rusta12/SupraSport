"""Операции с реестром пользователей tdm_bot.user_protection.

Все запросы параметризованы — значения передаются в execute(), а не
склеиваются со строкой запроса.
"""

import logging

from database.conn_db import (
    postgresql_to_data,
    postgresql_to_dataframe_params,
    postgresql_to_check
)
from protection.roles import ROLE_ANALYTIC

logger = logging.getLogger(__name__)

PROFILE_COLUMNS = [
    'id_user',
    'messenger_name',
    'id_role_access',
    'email',
    'phone',
    'workspace_id',
    'group_id',
    'created_at',
    'arhiv'
]

PROFILE_SELECT = """
    SELECT id_user, messenger_name, id_role_access, email, phone,
           workspace_id, group_id, created_at, arhiv
    FROM user_protection
    WHERE id_user = %s
"""


def to_user_id(raw) -> int:
    """Приведение идентификатора пользователя к int.

    Идентификаторы приходят из разных событий и могут прийти строкой —
    приводим один раз здесь, чтобы не получить промах по ключу в БД.
    """
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        logger.warning('Не удалось привести id пользователя к int: %r', raw)
        return None


def user_exists(user_id) -> bool:
    """Есть ли пользователь в реестре (архивные тоже считаются)"""
    user_id = to_user_id(user_id)
    if user_id is None:
        return False
    count = postgresql_to_check(
        'SELECT count(*) FROM user_protection WHERE id_user = %s', (user_id,)
    )
    return bool(count)


def add_user_bd(user_id, name=None, email=None, phone=None,
                workspace_id=None, group_id=None, role=ROLE_ANALYTIC) -> bool:
    """Регистрация пользователя с базовой ролью «Аналитик».

    Повторный вызов ничего не делает — ON CONFLICT защищает от дублей,
    которые возникли бы, если бот перезапустился между регистрацией
    и первым ответом.

    Роль по умолчанию 1, а не 0: состояния «без доступа» не существует.
    Возвращает True, если пользователь реально добавлен.
    """
    user_id = to_user_id(user_id)
    if user_id is None:
        return False

    postgresql_to_data(
        """
        INSERT INTO user_protection
            (id_user, messenger_name, id_role_access,
             email, phone, workspace_id, group_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id_user) DO NOTHING
        """,
        (user_id, name, role, email, phone, workspace_id, group_id)
    )
    return True


def get_user_profile(user_id):
    """Профиль пользователя как словарь либо None"""
    user_id = to_user_id(user_id)
    if user_id is None:
        return None

    df = postgresql_to_dataframe_params(
        PROFILE_SELECT, PROFILE_COLUMNS, (user_id,)
    )
    if df.shape[0] == 0:
        return None
    return df.iloc[0].to_dict()


def chek_user_profile(user_id):
    """Совместимость с именованием Telegram-версии"""
    return get_user_profile(user_id)


def get_user_access(user_id) -> int:
    """Уровень доступа пользователя.

    Для незарегистрированного возвращаем ROLE_ANALYTIC, а не 0: иначе новый
    пользователь упирался бы в нулевую роль и в отказ. Регистрация при этом
    всё равно выполняется отдельно (см. register_event_user).
    """
    user_id = to_user_id(user_id)
    if user_id is None:
        return ROLE_ANALYTIC

    role = postgresql_to_check(
        """
        SELECT id_role_access
        FROM user_protection
        WHERE id_user = %s AND arhiv = false
        """,
        (user_id,)
    )
    if role is None:
        return ROLE_ANALYTIC
    return int(role)


def chek_user_access(user_id) -> int:
    """Совместимость с именованием Telegram-версии"""
    return get_user_access(user_id)


def update_user_from_event(user_id, name=None, email=None, phone=None,
                           workspace_id=None, group_id=None) -> bool:
    """Дополнить профиль данными, пришедшими в событии группы.

    Имя приходит не в каждом событии, поэтому заполняются только те поля,
    которые реально переданы (COALESCE). Пустая строка считается отсутствием
    значения — иначе обновление затрёт уже сохранённое ФИО.
    """
    user_id = to_user_id(user_id)
    if user_id is None:
        return False

    postgresql_to_data(
        """
        UPDATE user_protection
        SET messenger_name = COALESCE(NULLIF(%s, ''), messenger_name),
            email          = COALESCE(NULLIF(%s, ''), email),
            phone          = COALESCE(NULLIF(%s, ''), phone),
            workspace_id   = COALESCE(%s, workspace_id),
            group_id       = COALESCE(%s, group_id)
        WHERE id_user = %s
        """,
        (name, email, phone, workspace_id, group_id, user_id)
    )
    return True


def is_archived(user_id) -> bool:
    """Помечен ли пользователь архивным (покинул чат)"""
    user_id = to_user_id(user_id)
    if user_id is None:
        return False

    arhiv = postgresql_to_check(
        'SELECT arhiv FROM user_protection WHERE id_user = %s', (user_id,)
    )
    return bool(arhiv)


def archive_user(user_id) -> bool:
    """Пользователь покинул чат — блокируем доступ, но сохраняем роль"""
    user_id = to_user_id(user_id)
    if user_id is None:
        return False

    postgresql_to_data(
        'UPDATE user_protection SET arhiv = true WHERE id_user = %s', (user_id,)
    )
    logger.info('Пользователь %s помечен архивным', user_id)
    return True


def restore_user(user_id) -> bool:
    """Пользователь вернулся — снимаем архивность с сохранением роли"""
    user_id = to_user_id(user_id)
    if user_id is None:
        return False

    postgresql_to_data(
        'UPDATE user_protection SET arhiv = false WHERE id_user = %s', (user_id,)
    )
    logger.info('Пользователь %s восстановлен', user_id)
    return True


def set_user_role(user_id, role) -> bool:
    """Ручная выдача роли. Используется только администратором вручную."""
    user_id = to_user_id(user_id)
    if user_id is None:
        return False

    postgresql_to_data(
        'UPDATE user_protection SET id_role_access = %s WHERE id_user = %s',
        (role, user_id)
    )
    logger.info('Роль пользователя %s изменена на %s', user_id, role)
    return True