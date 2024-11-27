from config import bot
from telebot import types
#Mod


def output_inline(message, SportClass):
	df = SportClass.df
	buttons = []
	for x in range(df.shape[0]):
		button = types.InlineKeyboardButton(
			text=df.loc[x, 'correct_name'], 
			callback_data=df.loc[x, 'menu'])
		buttons.append(button)
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	keyboard.add(*buttons)
	bot.send_message(message.chat.id, 
		f"Вот что у меня есть по Вашему запросу '{SportClass.text_user}':", 
		reply_markup=keyboard)

