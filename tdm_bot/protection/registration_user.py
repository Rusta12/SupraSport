"""Регистрация пользователей и вывод профиля.

Важная особенность TDM (в отличие от Telegram): событие `message` несёт
только `sender_id` — ни ФИО, ни e-mail в нём нет. Персональные данные
приходят в событиях группы (`group_user_join`, `group_users_add`,
`user_signed_up_to_workspace`) в payload.user.

Поэтому здесь три механизма:
  * user_cache — накопительный кэш профилей из событий группы;
  * register_event_user — гарантирует наличие строки в БД при любом событии,
    даже если ФИО ещё неизвестно (подставится позже);
  * fill_profile_from_chat — при первом обращении нового пользователя сразу
    берёт имя и телефон из состояния чата (opponent), не дожидаясь
    следующего перезапуска бота.
"""

import logging

from messenger_bot_api import MessageBotEvent

from protection.protection_insert import (
    add_user_bd,
    get_user_profile,
    update_user_from_event,
    user_exists,
    to_user_id
)
from protection.roles import ROLE_SENIOR_ANALYTIC, role_name, ROLE_DESCRIPTIONS

logger = logging.getLogger(__name__)

# Кэш профилей, собранных из событий группы: id -> {name, email, phone}
# Нужен потому, что событие message имени не содержит.
user_cache = {}


def _has_name(user_id) -> bool:
    """Заполнено ли ФИО (по кэшу либо по базе)."""
    if user_cache.get(user_id, {}).get('name'):
        return True
    profile = get_user_profile(user_id)
    return bool(profile and profile.get('messenger_name'))


def fill_profile_from_chat(event: MessageBotEvent, user_id) -> bool:
    """Дозаполнить messenger_name/phone из состояния текущего чата.

    Вызывается для новых пользователей: событие message имени не несёт,
    а ждать перезапуска бота (sync_names) — лишняя задержка. Состояние
    чата запрашивается один раз под конкретный (workspace_id, group_id)
    и разбирается тем же кодом, что и при старте (collect_opponent_data).

    Любая ошибка не роняет регистрацию — имя всё равно допишется
    при следующем перезапуске.
    """
    from database.conn_db import postgresql_to_data
    from protection.sync_names import collect_opponent_data

    try:
        state = event._request.get_state(event.workspace_id, event.group_id)
    except Exception:
        logger.warning('Не удалось получить состояние чата %s/%s для %s',
                       event.workspace_id, event.group_id, user_id,
                       exc_info=True)
        return False

    data = collect_opponent_data([state]) if isinstance(state, dict) else {}
    profile = data.get(user_id)
    if not profile:
        logger.info('В состоянии чата нет opponent для %s — имя допишется '
                    'при следующем старте', user_id)
        return False

    try:
        postgresql_to_data(
            """
            UPDATE user_protection
            SET messenger_name = COALESCE(NULLIF(%s, ''), messenger_name),
                phone         = COALESCE(NULLIF(%s, ''), phone)
            WHERE id_user = %s
            """,
            (profile.get('name'), profile.get('phone'), user_id)
        )
    except Exception:
        logger.warning('Не удалось записать имя/телефон для %s', user_id,
                       exc_info=True)
        return False

    # Кэш обновляем, чтобы не перезапрашивать состояние при каждом событии
    cached = user_cache.setdefault(user_id, {})
    if profile.get('name'):
        cached['name'] = profile['name']
    if profile.get('phone'):
        cached['phone'] = profile['phone']

    logger.info('Профиль из состояния чата: %s → %r', user_id, profile)
    return True


def _first_value(user_data: dict, *keys):
    """Достать первое непустое значение из payload.user.

    Набор ключей в TDM нужно уточнить на стенде (задача T-02), поэтому
    перебираем несколько вариантов написания вместо одного жёсткого.
    """
    for key in keys:
        value = user_data.get(key)
        if value not in (None, '', 'null'):
            return value
    return None


def extract_user_data(user_data) -> dict:
    """Разбор payload.user события группы в поля профиля"""
    if not isinstance(user_data, dict):
        return {}

    full_name = _first_value(user_data, 'name', 'fullName', 'displayName',
                             'fio', 'userName')
    email = _first_value(user_data, 'email', 'mail', 'eMail', 'userEmail')
    phone = _first_value(user_data, 'phone', 'phoneNumber', 'mobile',
                         'userPhone')
    user_id = _first_value(user_data, 'id', 'userId', 'senderId', 'user_id')

    return {
        'user_id': to_user_id(user_id),
        'name': full_name,
        'email': email,
        'phone': phone,
    }


def cache_user_profile(user_data, workspace_id=None, group_id=None) -> dict:
    """Запомнить профиль из события группы.

    Возвращает распарсенные данные, чтобы вызывающая сторона могла сразу
    зарегистрировать пользователя.
    """
    parsed = extract_user_data(user_data)
    if parsed.get('user_id') is None:
        return {}

    parsed['workspace_id'] = workspace_id
    parsed['group_id'] = group_id

    cached = user_cache.setdefault(parsed['user_id'], {})
    for key in ('name', 'email', 'phone'):
        if parsed.get(key):
            cached[key] = parsed[key]

    logger.info('Профиль из события группы: id=%s имя=%r',
                parsed['user_id'], parsed.get('name'))
    return parsed


def register_user_by_id(user_id, name=None, email=None,
                        phone=None, workspace_id=None, group_id=None) -> bool:
    """Регистрация пользователя по явно переданному id.

    Нужна для групповых событий: у них sender_id всегда None (это не тот
    человек, о ком событие), а сам участник лежит в payload.user.
    """
    user_id = to_user_id(user_id)
    if user_id is None:
        return False

    cached = user_cache.get(user_id, {})
    name = name or cached.get('name')
    email = email or cached.get('email')
    phone = phone or cached.get('phone')

    try:
        if not user_exists(user_id):
            add_user_bd(
                user_id,
                name=name,
                email=email,
                phone=phone,
                workspace_id=workspace_id,
                group_id=group_id
            )
            logger.info('Зарегистрирован новый пользователь %s (%r)',
                        user_id, name)
            return True

        update_user_from_event(
            user_id,
            name=name,
            email=email,
            phone=phone,
            workspace_id=workspace_id,
            group_id=group_id
        )
    except Exception:
        # Регистрация не должна ронять обработку события
        logger.exception('Не удалось зарегистрировать пользователя %s', user_id)
        return False

    return True


def register_event_user(event: MessageBotEvent, name=None,
                        email=None, phone=None) -> bool:
    """Гарантирует, что отправитель события есть в реестре.

    Вызывается на каждом входящем событии с текстом или командой.
    Если у нового пользователя ещё нет имени — сразу дозаполняем его
    из состояния чата, не дожидаясь перезапуска бота.
    """
    user_id = getattr(event, 'sender_id', None)
    if user_id is None:
        return False

    registered = register_user_by_id(
        user_id,
        name=name,
        email=email,
        phone=phone,
        workspace_id=getattr(event, 'workspace_id', None),
        group_id=getattr(event, 'group_id', None)
    )

    if not _has_name(user_id):
        fill_profile_from_chat(event, user_id)

    return registered


def add_user(event: MessageBotEvent) -> bool:
    """Совместимость с именованием Telegram-версии"""
    return register_event_user(event)


def profile_user_print(event: MessageBotEvent) -> str:
    """Текст профиля для команды /profile"""
    user_id = to_user_id(getattr(event, 'sender_id', None))
    profile = get_user_profile(user_id)

    if profile is None:
        return ('Пользователь не найден в реестре.\n'
                'Отправьте /start, чтобы зарегистрироваться.')

    role = profile.get('id_role_access')
    name = profile.get('messenger_name') or 'не указано'
    phone = profile.get('phone')
    created = profile.get('created_at')
    created_str = created.strftime('%d.%m.%Y %H:%M') if created else 'неизвестно'

    text = '[b]Ваш профиль[/b]\n'
    text += '[b]ФИО:[/b] {}\n'.format(name)
    if phone:
        text += '[b]Телефон:[/b] {}\n'.format(phone)
    text += '[b]ID в мессенджере:[/b] {}\n'.format(user_id)
    text += '[b]Роль:[/b] {} ({})\n'.format(
        role_name(role), ROLE_DESCRIPTIONS.get(role, '')
    )
    text += '[b]Дата регистрации:[/b] {}\n'.format(created_str)
    text += '[b]Статус:[/b] {}'.format(
        'архивный' if profile.get('arhiv') else 'активный'
    )

    if role != ROLE_SENIOR_ANALYTIC:
        text += ('\n\nПовышенный доступ ([b]Старший аналитик[/b]) выдаётся '
                 'по обращению к администратору.')

    return text


def profile_user(event: MessageBotEvent):
    """Обработчик команды /profile"""
    text = profile_user_print(event)
    event.reply_text(text)