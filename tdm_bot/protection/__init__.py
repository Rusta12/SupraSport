"""Модули регистрации пользователей и разграничения доступа."""

from protection.roles import (
    ROLE_ANALYTIC,
    ROLE_SENIOR_ANALYTIC,
    ROLE_NAMES,
    role_name
)
from protection.protection_insert import (
    user_exists,
    add_user_bd,
    get_user_profile,
    chek_user_profile,
    get_user_access,
    chek_user_access,
    update_user_from_event,
    is_archived,
    archive_user,
    restore_user,
    set_user_role
)
from protection.check_prot import (
    validation_user,
    validation_user_other,
    is_senior,
    is_admin,
    access_denied_text
)
from protection.registration_user import (
    register_event_user,
    add_user,
    profile_user,
    profile_user_print
)

__all__ = [
    'ROLE_ANALYTIC',
    'ROLE_SENIOR_ANALYTIC',
    'ROLE_NAMES',
    'role_name',
    'user_exists',
    'add_user_bd',
    'get_user_profile',
    'chek_user_profile',
    'get_user_access',
    'chek_user_access',
    'update_user_from_event',
    'is_archived',
    'archive_user',
    'restore_user',
    'set_user_role',
    'validation_user',
    'validation_user_other',
    'is_senior',
    'is_admin',
    'access_denied_text',
    'register_event_user',
    'add_user',
    'profile_user',
    'profile_user_print',
]