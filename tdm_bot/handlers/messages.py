import pandas as pd

from messenger_bot_api import MessageBotEvent, MessageRequest
# Модули
from bot_documents.default_text import ekp_text, ias_text, minsport_text
from database.select_ref import sport_token
from handlers.data_classs import SportClass
from handlers.callinline_button import output_inline_sport
from handlers.callbacks import mean_allocation


def receiving_messages(text:str) -> pd.DataFrame:
    """Поиск по тексту в справочнике меню"""
    text = text.lower()
    df = sport_token()
    df_sersh = df[(df['token_name'].str.contains(fr"{text}", na=False))]
    df_sersh = df_sersh[['menu', 'correct_name']]
    df_sersh.drop_duplicates(inplace=True)
    df_sersh = df_sersh.reset_index(drop=True)
    return df_sersh


def assemble_message(event: MessageBotEvent):
    """Основной алгоритм обработки текстовых сообщений"""
    #if validation_user(event, 1) is not True:
    #    return
    text = event.message_text
    if text is None:
        return

    text_lower = text.lower().strip()

    if text_lower in ['екп', 'календарь', 'кп', 'мероприятия']:
        return ekp_text(event)
    elif text_lower == 'иас':
        return ias_text(event)
    elif text_lower in ['емир', 'минспорт', 'гис', 'фгис', 'министерство']:
        return minsport_text(event)
    else:
        df = receiving_messages(text)
        if df.shape[0] != 0:
            if df.shape[0] == 1:
                data = df.loc[0, 'menu']
                return mean_allocation(event, data)
            elif df.shape[0] > 15:
                event.reply_text(
                    'Ваш запрос содержит большое количество вариантов, '
                    'пожалуйста дайте мне оптимальный контекст.'
                )
                return
            else:
                input_class = SportClass(
                    id_user=event.sender_id,
                    df=df,
                    text_user=text
                )
                return output_inline_sport(event, input_class)
        else:
            event.reply_text(
                '🚴‍♂️ По вашему запросу ничего не найдено. '
                'Попробуйте уточнить запрос.'
            )
            return

