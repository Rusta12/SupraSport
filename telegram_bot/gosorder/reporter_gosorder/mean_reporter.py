from config import bot
from telebot import types
import os
#Mod
from gosorder.reporter_gosorder.report_refence import firm_report, sport_report, global_report, kpi_gos_mean
from database.attributs import upd_loger_finishhim
from protection.check_prot import validation_user
from gosorder.reporter_gosorder.kpi_gosorder import kpi_chronology

def gos_menu_reporter(message):
	keyboard = types.InlineKeyboardMarkup()
	reg1 = types.InlineKeyboardButton(text="Отчет по организациям", callback_data="gos_report_shcool")
	reg2 = types.InlineKeyboardButton(text="Отчет по виду спорта", callback_data="gos_report_sport")
	reg3 = types.InlineKeyboardButton(text="Общий отчет", callback_data="gos_download_data")
	back = types.InlineKeyboardButton(text="Отмена операции", callback_data="escape")
	keyboard.row(reg1, reg2)
	keyboard.row(reg3)
	keyboard.row(back)
	bot.send_message(message.chat.id,
		"Выберете необходимый форму сводного отчета",
		reply_markup=keyboard)

def gos_menu_reporter_global(message):
	keyboard = types.InlineKeyboardMarkup()
	reg1 = types.InlineKeyboardButton(text="Представить первичный отчет", callback_data="gos_report_global")
	back = types.InlineKeyboardButton(text="Отмена операции", callback_data="escape")
	keyboard.row(reg1)
	keyboard.row(back)
	bot.send_message(message.chat.id,
		"⚠️Внимание этот отчет будет большим вы уверены, что хотите получить его?",
		reply_markup=keyboard)	


def gos_reports_shcools(message):
	if validation_user(message, 1) == True:
		pass
	else:
		return
	with open('./bot_documents/gif/robot_y4it.mp4', 'rb') as gif:
		msv = bot.send_video(message.chat.id, gif, None)
	try:
		df = firm_report()
		tmp_df = f"./gosorder/reporter_gosorder/Temp/ГЗ_по_школам_{message.chat.id}.xlsx"
		df.to_excel(tmp_df)
		with open(tmp_df, 'rb') as file:
			bot.send_document(message.chat.id, file)
		os.remove(tmp_df)
		bot.delete_message(message.chat.id, msv.message_id)
		upd_loger_finishhim(message, 'gos_report_shcool', '0')
	except Exception as e:
		bot.delete_message(message.chat.id, msv.message_id)
		upd_loger_finishhim(message, 'gos_report_shcool', '0', e)


def gos_reports_sports(message):
	if validation_user(message, 1) == True:
		pass
	else:
		return
	with open('./bot_documents/gif/robot_y4it.mp4', 'rb') as gif:
		msv = bot.send_video(message.chat.id, gif, None)
	try:
		df = sport_report()
		tmp_df = f"./gosorder/reporter_gosorder/Temp/ГЗ_по_видам_спорта_{message.chat.id}.xlsx"
		df.to_excel(tmp_df)
		with open(tmp_df, 'rb') as file:
			bot.send_document(message.chat.id, file)
		os.remove(tmp_df)
		bot.delete_message(message.chat.id, msv.message_id)
		upd_loger_finishhim(message, 'gos_report_sport', '0')
	except Exception as e:
		bot.delete_message(message.chat.id, msv.message_id)
		upd_loger_finishhim(message, 'gos_report_sport', '0', e)



def gos_reports_global(message):
	if validation_user(message, 1) == True:
		pass
	else:
		return
	with open('./bot_documents/gif/robot_y4it.mp4', 'rb') as gif:
		msv = bot.send_video(message.chat.id, gif, None)
	try:
		df = global_report()
		tmp_df = f"./gosorder/reporter_gosorder/Temp/ГЗ_первичный_{message.chat.id}.xlsx"
		df.to_excel(tmp_df, index=False)
		with open(tmp_df, 'rb') as file:
			bot.send_document(message.chat.id, file)
		os.remove(tmp_df)
		bot.delete_message(message.chat.id, msv.message_id)
		upd_loger_finishhim(message, 'gos_download_data', 'gos_report_global')
	except Exception as e:
		bot.delete_message(message.chat.id, msv.message_id)
		upd_loger_finishhim(message, 'gos_download_data', 'gos_report_global', e)


def gos_kpi_chronology(message):
	if validation_user(message, 1) == True:
		pass
	else:
		return
	try:
		df = kpi_gos_mean()
		image_name = kpi_chronology(message, df)
		with open(image_name, 'rb') as phote:
			bot.send_photo(message.chat.id, phote)
		os.remove(image_name)
		upd_loger_finishhim(message, 'gos_display_chronology', '0')
	except Exception as e:
		bot.send_message(message.chat.id, text=f'Что то пошло не так код ошибки\n{e}')
		upd_loger_finishhim(message, 'gos_display_chronology', '0', e)


