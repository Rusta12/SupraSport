from config import bot
from telebot import types
import re
#Модули
from gosorder.reception_gos import gos_reception
from original_request.sport_menu.mean_sport_menu import print_sport 
from original_request.school_menu.mean_school_menu import print_school
from fedorder.reception_fed import fed_reception

#Функция распределения
def mean_allocation(message, data:str):
	#Главные Шаблоны распределения
	patern_gos = r'gos_'
	gos = re.match(patern_gos, data)
	#=============================
	patern_sport = r'sport_menu_'
	sport = re.match(patern_sport, data)
	patern_sсhool = r'sсhool_menu_'
	school = re.match(patern_sсhool, data)
	patern_fed = 'fed_'
	fed = re.match(patern_fed, data)
	#=============================
	#Цикл распределения по функциям
	if gos:
		return gos_reception(message, data)
	elif sport:
		return print_sport(message, data)
	elif school:
		return print_school(message, data)
	elif patern_fed:
		return fed_reception(message, data)
	else:
		pass
