from config import bot
from telebot import types
#Mod
from inline_callback import callback_inline

def fed_menu_general(message):
    keyboard = types.InlineKeyboardMarkup()
    reg0 = types.InlineKeyboardButton(text="Загрузить файл с Федерациями", callback_data="fed_load_data")
    reg1 = types.InlineKeyboardButton(text="Получить отчет в файле по федерациям", callback_data="fed_report_data")
    back = types.InlineKeyboardButton(text="Отмена операции", callback_data="escape")
    keyboard.row(reg0)
    keyboard.row(reg1)
    keyboard.row(back)
    bot.send_message(message.chat.id,
                     "Выберите что необходимо сделать.",
                     reply_markup=keyboard)
    bot.register_chosen_inline_handler(message, callback_inline)

