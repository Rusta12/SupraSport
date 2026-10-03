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
#from protection.registration_user import add_user, profile_user


def start_handler(event: MessageBotEvent):
    """Обработчик команды /start"""
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

    menu_gos_temp(event)
    #add_user(event)


def profile_handler(event: MessageBotEvent):
    """Обработчик команды /profile"""
    #profile_user(event)


def menu_gos_temp(event: MessageBotEvent):
    """Временное меню с кнопками"""
    buttons = [
        InlineMessageButton(id=1, label="ГОС задание", callback_data="gos_menu"),
        InlineMessageButton(id=2, label="Федерации", callback_data="fed_menu"),
    ]
    message = MessageRequest(
        text="Попробуй у меня что-нибудь спросить",
        buttons=buttons
    )
    event.reply_text_message(message)


def message_handler(event: MessageBotEvent):
    """Обработчик текстовых сообщений"""
    logger.info(f'Получено текстовое сообщение: {event.message_text}')
    return assemble_message(event)


def click_button_handler(event: MessageBotEvent):
    """Обработчик нажатий на кнопки"""
    from handlers.callbacks import mean_allocation
    selected = event.selected_button
    if selected and selected.callback_data:
        event.reply_text(f'Выбор сделан ✅')
        logger.info(f'Пользователь нажал кнопку {selected}')
        return mean_allocation(event, selected.callback_data)


def group_me_add_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_me_remove_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_history_clear_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_delete_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_user_remove_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_users_add_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_user_join_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def group_user_leave_handler(event):
    event.confirm_event(event.workspace_id, event.group_id, event.event_id)


def update_message_handler(event):
    event.confirm_event_from_current_group(event.event_id)


def delete_message_handler(event):
    event.confirm_event_from_current_group(event.event_id)


def main():
    logger.info('🚀 Запуск бота SupraSport для мессенджера tdm.mos.ru ...')

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

    logger.info('✅ Бот запущен и ожидает сообщений...')
    bot.start()

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
