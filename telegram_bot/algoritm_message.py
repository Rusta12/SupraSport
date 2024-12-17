from config import bot
from telebot import types, util
import time
#ChatGPT
from gptYa import ya_gpt
#Mod
from gosorder.menu_gos_inline import gos_menu_general
from fedorder.menu_fed_inline import fed_menu_general
from protection.check_prot import validation_user
from original_request.class_reg  import receiving_messages, SportClass
from original_request.output_reg import output_inline
from callback_allocation import mean_allocation
from ekp.menu_mean_ekp import ekp_text
from database.attributs import upd_loger_finishhim, add_loger




def algoritm_ai(message):
    if validation_user(message, 1) == True:
        pass
    else:
        return

    if message.text == 'ГОС задание' or message.text.lower() == 'гос' or message.text.lower() == 'задание' or message.text.lower() == 'гз ':
        bot.delete_message(message.chat.id, message.message_id)
        return gos_menu_general(message)
    elif message.text.lower() == 'фед' or message.text.lower() == 'федерации' or message.text.lower() == 'федера':
        bot.delete_message(message.chat.id, message.message_id)
        return fed_menu_general(message)
    elif message.text.lower() == 'екп':
        bot.delete_message(message.chat.id, message.message_id)
        return ekp_text(message)
    else:
        df =  receiving_messages(message.text)
        if df.shape[0] != 0:
            if df.shape[0] == 1:
                data = df.loc[0, 'menu']
                return mean_allocation(message, data)

            elif df.shape[0] > 15:
                bot.send_message(message.chat.id, 
                    'Ваш запрос содержит большое количество вариантов, пожалуйста дайте мне оптимальный контекст.')
                bot.delete_message(message.chat.id, message.message_id)
                return

            else:
                bot.delete_message(message.chat.id, message.message_id)
                input_class = SportClass(id_user = message.chat.id, df = df, text_user = message.text)
                return output_inline(message, input_class)

        elif df.shape[0] == 0:
            msg = bot.send_message(message.chat.id, '🚴‍♂️ Обрабатываю Ваш запрос ...')
            add_loger(message, 'GPT', message.text)
            try:
                theb_gpt(message)
                bot.delete_message(message.chat.id, msg.message_id)
                return
            except Exception as e:
                bot.send_message(message.chat.id, f"Сервер занят. Попробуйте позже. \nКод ошибки:\n{e}")
                bot.delete_message(message.chat.id, msg.message_id)
                return

def split_text(text, max_length=4096):
    # Разделяем текст на части, учитывая лимиты Telegram
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def theb_gpt(message): 
    output = ya_gpt(message.text)
    if output:  # Проверяем, что output не пуст
        splitted_text = util.smart_split(output, chars_per_string=2000)
        for text in splitted_text:
            bot.send_message(message.chat.id, text=text, parse_mode='Markdown')
            upd_loger_finishhim(message, 'GPT', message.text)
    else:
        bot.send_message(message.chat.id, "Не удалось получить ответ от GPT.")
        upd_loger_finishhim(message, 'GPT', message.text, 'Не удалось получить ответ от GPT.')
    return

