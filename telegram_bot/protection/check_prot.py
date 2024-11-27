from telebot import types
from config import bot
#Mod
from protection.protection_insert import chek_user_access


#Общий доступ
def validation_user(message, lvl: int):
	user_id = message.chat.id
	access = chek_user_access(user_id) 
	if access >= lvl:
		return True
	elif access < lvl:
		bot.send_message(message.chat.id, text='Вашего уровня доступа недостаточно.')
		return False
	else:
		bot.send_message(message.chat.id, text='Доступ запрещен.')
		return False

#Доступ для инлайн кнопок
def validation_user_calback(user_id, lvl: int):
	access = chek_user_access(user_id) 
	if access >= lvl:
		return True
	elif access < lvl:
		bot.send_message(user_id, text='Вашего уровня доступа недостаточно.')
		return False
	else:
		bot.send_message(user_id, text='Доступ запрещен.')
		return False

#Доступ для остальных случаев
def validation_user_other(user_id, lvl: int):
	access = chek_user_access(user_id) 
	if access >= lvl:
		return True
	elif access < lvl:
		return False
	else:
		return False