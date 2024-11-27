from config import bot
from telebot import types
import os
#Mod
from database.conn_db import copy_from_file
from database.attributs import upd_user_attribute_name_two, upd_user_attribute_name_three, upd_loger_finishhim
from database.attributs_load import load_menu_attribut_two
from gosorder.update_gosorder.read_gos import general_concat
from gosorder.update_gosorder.check_data import check_name_file, arhiv_data
from gosorder.update_gosorder.reference import name_file_to_id_tuple, total_gos_mean
from protection.check_prot import validation_user
from gosorder.update_gosorder.colum_gos_order import col_bd


def gos_menu_reload(message):
	keyboard = types.InlineKeyboardMarkup()
	reg1 = types.InlineKeyboardButton(text="Повторить попытку", callback_data="gos_load_data")
	reg2 = types.InlineKeyboardButton(text="Заменить файл-данные", callback_data="gos_reload_data")
	back = types.InlineKeyboardButton(text="Отмена операции", callback_data="escape")
	keyboard.row(reg1, reg2)
	keyboard.row(back)
	bot.send_message(message.chat.id,
		"⛔️ Данный файл уже был загружены в базу."
		"\nЕсли данные нужно заменить воспользуйтесь функцией - «Заменить файл-данные»",
		reply_markup=keyboard)



def menu_upload_file(message):
    if validation_user(message, 2) == True:
        pass
    else:
        return
    bot.send_message(
		message.chat.id,
		text='📌Перед отправкой файла убедитесь, пожалуйста, в следующем'
	          '\n1. Файл должен быть в виде «excel».'
	          '\n2. Имя файла должно обязательно содержать месяц и год например: «Свод ГЗ 1 января 2023»'
	          '\n3. Если файл с таким именем уже загружен то данные будут заменены, проверте имя файла перед отпавкой'
	          )
    #тут инструкция и сообщение о содержании файла
    bot.send_message(message.chat.id, text="Отправьте мне файл.")
    @bot.message_handler(content_types=['document'])
    def send_file_gos(message):
    	try:
    		file_info = bot.get_file(message.document.file_id)
    		downloaded_file = bot.download_file(file_info.file_path)
    		path_file = f'./gosorder/update_gosorder/Temp/{message.document.file_name}'
    		if chek_file(message, path_file, downloaded_file) == 'gos_menu_reload':
    			return gos_menu_reload(message)
    		else:
    			pass
    		msg = bot.reply_to(message, "Файл получен, ожидайте пожалуйста!")
    		with open('./bot_documents/gif/batut.mp4', 'rb') as gif:
    			msv = bot.send_video(message.chat.id, gif, None)
    		process_file(message, path_file)
    		bot.send_message(message.chat.id,
    			f"Файл успешно обработан. {message.document.file_name}")
    		bot.delete_message(message.chat.id, msg.message_id)
    		bot.delete_message(message.chat.id, msv.message_id)
    		upd_loger_finishhim(message, 'gos_load_data', 'load_data')
    		print_upload_data(message)
    	except Exception as e:
    		upd_loger_finishhim(message, 'gos_load_data', 'load_data', e)
    		bot.send_message(message.chat.id, f"Что-то пошло не так. Попробуйте снова. \nКод ошибки:\n{e}")
    		os.remove(path_file)
    		bot.delete_message(message.chat.id, msg.message_id)
    		bot.delete_message(message.chat.id, msv.message_id)

def menu_reload_file(message):
    if validation_user(message, 2) == True:
        pass
    else:
        return
    path_file = load_menu_attribut_two(message, 'gos_load_data', 'reload_data')
    msg = bot.send_message(message.chat.id, "Файл в обработке, ожидайте пожалуйста!")
    try:
    	with open('./bot_documents/gif/batut.mp4', 'rb') as gif:
    		msv = bot.send_video(message.chat.id, gif, None)
    	id_gos = check_name_file(path_file)
    	process_file(message, path_file)
    	arhiv_data(id_gos)
    	bot.send_message(message.chat.id, f"Файл успешно обработан.")
    	bot.delete_message(message.chat.id, msg.message_id)
    	bot.delete_message(message.chat.id, msv.message_id)
    	upd_loger_finishhim(message, 'gos_load_data', 'reload_data')
    	print_upload_data(message)
    except Exception as e:
    	upd_loger_finishhim(message, 'gos_load_data', 'reload_data', e)
    	os.remove(path_file)
    	bot.delete_message(message.chat.id, msg.message_id)



def chek_file(message, path_file, downloaded_file):
	with open(path_file, 'wb') as new_file:
		new_file.write(downloaded_file)
	upd_user_attribute_name_two(message, 'gos_load_data', path_file)
	chek_id_gos = check_name_file(path_file)
	if len(chek_id_gos) != 0:
		n = 'gos_menu_reload'
		return n
	elif len(chek_id_gos) == 0:
		bot.send_message(message.chat.id, text="Файл прошел проверку успешно.")
		pass


def process_file(message, path_file):
	df = load_data_df(path_file)
	load_data_bd(df)
	os.remove(path_file)


def load_data_df(path_file):
	df = general_concat(path_file)
	return df

def load_data_bd(df):
	copy_from_file(df, 'supra.gos_order', col_bd)


def print_upload_data(message):
	df = total_gos_mean()
	name_head = f"Общая информация по загруженным данным\n<b>{df.loc[0, 'Гос задание']}</b>"\
				f"\nОбщая численность занимающихся - <b>{df.loc[0, 'Общий']}</b>\nиз них:\n"
	name_np = f"этап начальной подготовки – {df.loc[0, 'НП']}\n"
	name_te = f"тренировочный этап – {df.loc[0, 'ТЭ']}\n"
	name_cc = f"этап совершенствования спортивного мастерства – {df.loc[0, 'СС']}\n"
	name_vsm = f"этап высшего спортивного мастерства – {df.loc[0, 'ВСМ']}\n"
	name_gw = f"государственная работа – {df.loc[0, 'Гос работа']}\n"
	name_context = (name_head+name_np+name_te+name_cc+name_vsm+name_gw)
	bot.send_message(message.chat.id, name_context, parse_mode='HTML')



