"""Уровни доступа пользователей.

Единственный источник правды для текстов: названия ролей не должны
расходиться между /profile, отказами и отчётами. В БД те же значения
засеяны в tdm_bot.role_access (см. db/init/tdm_bot_schema.sql).
"""

# Аналитик — основная рабочая роль, весь текущий функционал.
ROLE_ANALYTIC = 1

# Старший аналитик — повышенный доступ: закрытая информация.
ROLE_SENIOR_ANALYTIC = 2

ROLE_NAMES = {
    ROLE_ANALYTIC: 'Аналитик',
    ROLE_SENIOR_ANALYTIC: 'Старший аналитик',
}

ROLE_DESCRIPTIONS = {
    ROLE_ANALYTIC: 'основная рабочая роль, доступ ко всему текущему функционалу',
    ROLE_SENIOR_ANALYTIC: 'повышенный доступ: информация, недоступная обычному аналитику',
}


def role_name(role) -> str:
    """Название роли по её числовому значению"""
    return ROLE_NAMES.get(role, 'Неизвестная роль ({})'.format(role))


def is_valid_role(role) -> bool:
    """Проверка, что значение входит в известный набор ролей"""
    return role in ROLE_NAMES