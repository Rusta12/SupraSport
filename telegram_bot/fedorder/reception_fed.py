from config import bot
#Mod
from database.attributs import add_loger
from fedorder.mean_fed import fed_upload_file

def fed_reception(message, fed_data:str):
	if fed_data == 'fed_load_data':
		add_loger(message, fed_data, 'reload_data')
		return fed_upload_file(message)
	else:
		return