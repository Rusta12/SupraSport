from config import bot
#Mod
from gosorder.update_gosorder.mean_gos import menu_upload_file, menu_reload_file
from gosorder.reporter_gosorder.mean_reporter import gos_menu_reporter, gos_reports_shcools, gos_reports_sports
from gosorder.reporter_gosorder.mean_reporter import gos_menu_reporter_global, gos_reports_global
from gosorder.reporter_gosorder.mean_reporter import gos_kpi_chronology
from database.attributs import add_loger, upd_user_attribute_name_one


def gos_reception(message, gos_data:str):
	if gos_data == 'gos_load_data':
		add_loger(message, gos_data, 'load_data')
		return menu_upload_file(message)

	elif gos_data == 'gos_reload_data':
		upd_user_attribute_name_one(message, 'gos_load_data', 'reload_data')
		return menu_reload_file(message)

	elif gos_data == 'gos_report_data':
		return gos_menu_reporter(message)

	elif gos_data == 'gos_report_shcool':
		add_loger(message, gos_data)
		return gos_reports_shcools(message)

	elif gos_data == 'gos_report_sport':
		add_loger(message, gos_data)
		return gos_reports_sports(message)

	elif gos_data == 'gos_download_data':
		add_loger(message, gos_data)
		return gos_menu_reporter_global(message)

	elif gos_data == 'gos_report_global':
		upd_user_attribute_name_one(message, 'gos_download_data', 'gos_report_global')
		return gos_reports_global(message)

	elif gos_data == 'gos_display_chronology':
		add_loger(message, gos_data)
		return gos_kpi_chronology(message)

	else:
		print(f'{gos_data} команда не обнаружена в gos_reception')
