from config import bot
from telebot import types
#Mod
from inline_callback import callback_inline

def gos_menu_general(message):
    keyboard = types.InlineKeyboardMarkup()
    reg0 = types.InlineKeyboardButton(text="Загрузить файл с гос заданием", callback_data="gos_load_data")
    reg1 = types.InlineKeyboardButton(text="Получить сводный гос отчет в файле", callback_data="gos_report_data")
    reg2 = types.InlineKeyboardButton(text="Показать хронологию по гос заданию", callback_data="gos_display_chronology")
    back = types.InlineKeyboardButton(text="Отмена операции", callback_data="escape")
    keyboard.row(reg0)
    keyboard.row(reg1)
    keyboard.row(reg2)
    keyboard.row(back)
    bot.send_message(message.chat.id,
                     "Выберите что необходимо сделать.",
                     reply_markup=keyboard)
    bot.register_chosen_inline_handler(message, callback_inline)


