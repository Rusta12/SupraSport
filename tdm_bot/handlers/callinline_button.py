from messenger_bot_api import MessageBotEvent, MessageRequest, InlineMessageButton
# Модули
# SportClass живёт в handlers.data_classs, а не в handlers.messages —
# прежний импорт отсюда падал бы с ImportError
from handlers.data_classs import SportClass


def output_inline_sport(event: MessageBotEvent, input_class: SportClass):
    """Вывод inline кнопок с вариантами ответа"""
    df = input_class.df
    buttons = []
    for i in range(df.shape[0]):
        name = df.loc[i, 'correct_name']
        menu = df.loc[i, 'menu']
        buttons.append(
            InlineMessageButton(id=i + 1, label=name, callback_data=menu)
        )
    # Добавляем кнопку отмены так как кнопки удалить не можем то нет смысла добовлять отмену
    #buttons.append(
    #    InlineMessageButton(id=len(buttons) + 1, label="Отмена", callback_data="escape")
    #)
    message = MessageRequest(
        text=f'По вашему запросу «{input_class.text_user}» найдено несколько вариантов. Выберите нужный:',
        buttons=buttons
    )
    event.reply_text_message(message)
