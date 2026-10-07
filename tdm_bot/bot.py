import logging
import sys

from messenger_bot_api import *

import settings

# Настройка логирования
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

logger = logging.getLogger('suprasport_bot')

# Импорт модулей бота
from handlers.messages import assemble_message
from mime_types import apply_mime_workaround
from database.insert_log import (
    log_command,
    log_button,
    CATEGORY_SERVICE
)
from protection.registration_user import (
    register_event_user,
    register_user_by_id,
    profile_user,
    cache_user_profile,
    extract_user_data
)
from protection.protection_insert import archive_user, restore_user


def start_handler(event: MessageBotEvent):
    """Обработчик команды /start"""
    register_event_user(event)
    log_command(event, '/start', category=CATEGORY_SERVICE)

    try:
        with open('./bot_documents/logo.jpg', 'rb') as photo:
            from messenger_bot_api import Image
            img = Image('logo.jpg', photo.read())
            event.send_image_message(
                event.workspace_id,
                event.group_id,
                img,
                MessageRequest('')
            )
    except Exception as e:
        logger.warning(f'Не удалось отправить фото: {e}')

    try:
        with open('./bot_documents/Text_bot_information.txt', 'rt', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        content = ''
    event.reply_text(
        f"Приветствую Вас!\n"
        "Я — продвинутый спортивный бот Спортивного управления Москомспорта и разбирающийся в статистике.\n"
        "\n=================================================\n"
        "В настоящее время нахожусь в разработке, по вопросам обращайтесь к моему создателю.\n"
        "Закрепи меня в свой чат лист, что бы мы не потерялись 👍"
    )

    if content:
        event.reply_text(content)

    menu_mean(event)


def profile_handler(event: MessageBotEvent):
    """Обработчик команды /profile"""
    register_event_user(event)
    log_command(event, '/profile', category=CATEGORY_SERVICE)
    profile_user(event)


def menu_mean(event: MessageBotEvent):
    """Основное меню бота: выгрузки-списки.

    Кнопки расширяются добавлением пары (label, callback_data) и ветки
    в handlers/callbacks.py::mean_allocation. «График отпусков» — в обдумывании.
    """
    buttons = [
        InlineMessageButton(id=1, label="Учреждения Москомспорта",
                            callback_data="list_org_moskomport"),
        InlineMessageButton(id=2, label="Другие учреждения",
                            callback_data="list_org_other"),
        InlineMessageButton(id=3, label="Список Федераций",
                            callback_data="list_federations"),
    ]
    message = MessageRequest(
        text="Попробуй у меня что-нибудь спросить",
        buttons=buttons
    )
    event.reply_text_message(message)


def message_handler(event: MessageBotEvent):
    """Обработчик текстовых сообщений"""
    logger.info(f'Получено текстовое сообщение: {event.message_text}')
    register_event_user(event)
    return assemble_message(event)


def click_button_handler(event: MessageBotEvent):
    """Обработчик нажатий на кнопки"""
    from handlers.callbacks import mean_allocation
    selected = event.selected_button
    if selected and selected.callback_data:
        # ClickButtonEventHandler перехватывает событие раньше MessageHandler,
        # поэтому message_handler сюда не доходит — регистрируем здесь же
        register_event_user(event)
        log_button(event, selected.callback_data)
        event.reply_text(f'Выбор сделан ✅')
        logger.info(f'Пользователь нажал кнопку {selected}')
        return mean_allocation(event, selected.callback_data)


def _register_group_user(event, user_data):
    """Регистрация участника группового события.

    У групповых событий sender_id всегда None — это не тот человек, о ком
    событие, поэтому id берём из payload.user.
    """
    parsed = extract_user_data(user_data)
    user_id = parsed.get('user_id')
    if not user_id:
        return None

    cache_user_profile(user_data, workspace_id=event.workspace_id,
                       group_id=event.group_id)
    register_user_by_id(
        user_id,
        name=parsed.get('name'),
        email=parsed.get('email'),
        phone=parsed.get('phone'),
        workspace_id=event.workspace_id,
        group_id=event.group_id
    )
    return user_id


def group_me_add_handler(event):
    """Бот добавлен в чат — запоминаем участников"""
    _register_group_user(event, event.get_payload_data('user'))
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_me_remove_handler(event):
    """Бот удалён из чата"""
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_history_clear_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_delete_handler(event):
    """Чат удалён"""
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_user_remove_handler(event):
    """Пользователь исключён из чата — блокируем доступ"""
    _register_group_user(event, event.get_payload_data('user') or {})
    parsed = extract_user_data(event.get_payload_data('user') or {})
    if parsed.get('user_id'):
        archive_user(parsed['user_id'])
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_users_add_handler(event):
    """Пользователи добавлены в чат — регистрируем как Аналитиков"""
    for user_data in (event.get_payload_data('users') or []):
        _register_group_user(event, user_data)
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_user_join_handler(event):
    """Пользователь вошёл в чат — регистрируем и снимаем архивность"""
    user_id = _register_group_user(event, event.get_payload_data('user') or {})
    if user_id:
        restore_user(user_id)
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_user_leave_handler(event):
    """Пользователь вышел из чата сам — доступ блокируется, роль сохраняется"""
    parsed = extract_user_data(event.get_payload_data('user') or {})
    if parsed.get('user_id'):
        archive_user(parsed['user_id'])
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def user_signed_up_handler(event):
    """Пользователь зарегистрировался в рабочем пространстве"""
    _register_group_user(event, event.get_payload_data('user'))
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def update_message_handler(event):
    event.confirm_event_from_current_group(event.event_id)


def delete_message_handler(event):
    event.confirm_event_from_current_group(event.event_id)


def main():
    logger.info('🚀 Запуск бота SupraSport для мессенджера tdm.mos.ru ...')

    # MIME-фолбэк для файловых вложений (xlsx и т.п.) — см. mime_types.py
    apply_mime_workaround()

    # Схему tdm_bot создаёт db/init/tdm_bot_schema.sql. Postgres выполняет
    # эти скрипты только при первой инициализации пустого тома, поэтому на
    # уже существующей базе схему нужно применить вручную:
    #   docker exec -i suprasport_db psql -U supra_sport -d supra_sport \
    #       -f db/init/tdm_bot_schema.sql

    bot = Application(
        token=settings.TOKEN,
        request_kwargs={
            'api_base_url': settings.REST,
            'sse_base_url': settings.SSE,
            'file_upload_base_url': settings.FILE,
        }
    )

    # Регистрация обработчиков кнопок (первым, чтобы перехватывать до MessageHandler)
    bot.add_handler(ClickButtonEventHandler(click_button_handler))

    # Регистрация команд
    bot.add_handler(CommandHandler('start', start_handler))
    bot.add_handler(CommandHandler('profile', profile_handler))

    # Регистрация обработчика текстовых сообщений
    bot.add_handler(MessageHandler(message_handler))

    # Регистрация системных обработчиков
    bot.add_handler(UpdateMessageEventHandler(update_message_handler))
    bot.add_handler(DeleteMessageEventHandler(delete_message_handler))
    bot.add_handler(GroupMeAddHandler(group_me_add_handler))
    bot.add_handler(GroupMeRemoveHandler(group_me_remove_handler))
    bot.add_handler(GroupHistoryClearHandler(group_history_clear_handler))
    bot.add_handler(GroupDeleteHandler(group_delete_handler))
    bot.add_handler(GroupUserRemoveHandler(group_user_remove_handler))
    bot.add_handler(GroupUsersAddHandler(group_users_add_handler))
    bot.add_handler(GroupUserJoinHandler(group_user_join_handler))
    bot.add_handler(GroupUserLeaveHandler(group_user_leave_handler))
    bot.add_handler(UserSignedUpToWorkspaceHandler(user_signed_up_handler))

    logger.info('✅ Бот запущен и ожидает сообщений...')
    bot.start()

    # Синхронизация ФИО: события мессенджера не несут имён (только sender_id),
    # единственный источник — opponent в состояниях чатов API. Выполняется
    # при каждом старте; UPDATE идёт только для пустых/изменившихся имён.
    # Используем тот же bot._request, чтобы не плодить лишний сетевой слой.
    try:
        from protection.sync_names import sync_user_names
        sync_user_names(bot._request)
    except Exception:
        logger.warning('Синхронизация ФИО не выполнена, продолжаем без неё',
                       exc_info=True)

    # Держим основной поток живым
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('🛑 Бот остановлен.')
        bot.stop()


if __name__ == '__main__':
    main()
