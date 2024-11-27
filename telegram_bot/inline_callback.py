from telebot import types
from config import bot
#Mod
from callback_allocation import mean_allocation


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    return mean_allocation(call.message, call.data)
