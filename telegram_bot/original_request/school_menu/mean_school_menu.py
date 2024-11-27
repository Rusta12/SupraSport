from config import bot
from telebot import types
import os
import pandas as pd
#Mod
from original_request.reference_reg import school_name_school, school_mean_sport, school_mean_curator, school_mean_sport_past
from original_request.reference_reg import school_mean_firm, school_led_firm
from database.attributs import upd_loger_finishhim, add_loger
from original_request.school_menu.kpi_school_menu import get_school_kpi


def school_context_contact(school_menu:int):
    df = school_mean_firm(school_menu)
    name_full = df.loc[0, 'name_full']
    contakt_email = df.loc[0, 'contakt_email']
    contakt_tel = df.loc[0, 'contakt_tel']
    contakt_url = df.loc[0, 'contakt_url']
    firm_url = df.loc[0, 'firm_url']
    ogrn = df.loc[0, 'ogrn']
    context = f"<a href='{firm_url}'>{name_full}</a>\n"\
            f"ОГРН: {ogrn}\n"\
            f"<b>Почта:</b> {contakt_email}\n"\
            f"<b>Сайт:</b> {contakt_url}\n"\
            f"<b>Телефоны:</b> {contakt_tel}\n\n"
    return context

def school_led(school_menu:int):
    df = school_led_firm(school_menu)
    led_job = df.loc[0, 'name_job']
    led_name = df.loc[0, 'name_led']
    led_cotakt = df.loc[0, 'led_cotakt']
    led_email = df.loc[0, 'led_mail']
    context = f"<b>{led_job.title()}</b>\n{led_name}\n{led_cotakt}\n{led_email}\n\n"
    return context


def school_context_curators(school_menu:int):
	df = school_mean_curator(school_menu)
	name_curator = df.loc[0, 'name_curator']
	contakt_tel = df.loc[0, 'contakt_tel']
	contakt_email = df.loc[0, 'contakt_email']
	context = f'<b>Куратор Спортивного управления:</b>\n{name_curator}, \n{contakt_tel}\n{contakt_email}\n\n'
	return context

def school_contex_count(name_school:str, df_school):
	if df_school.shape[0] > 1:
		list_sh = []
		for i in range(df_school.shape[0]):
			sport_sum = f"{df_school.loc[i, 'Вид спорта']} - {df_school.loc[i, 'Общая численность']} чел."
			list_sh.append(sport_sum)
		name_sh = '\n- '.join(list_sh)
		name_sh = f'\n- {name_sh}'
		context = f"Виды спорта:\n{name_sh}"
		return context
		
	elif df_school.shape[0] == 1:
		context = f"Вид спорта:"\
					f"\n{df_school.loc[0, 'Вид спорта']} - {df_school.loc[0, 'Общая численность']} чел."
		return context


def school_mean_reg(school_menu:int):
    #Загрузска данных
    name_school = school_name_school(school_menu)
    df_school = school_mean_sport(school_menu)
    #Загаловок
    context_header = f"Информационная справка по учреждению: \n<b>{name_school}</b>\n\n"
    #Общие сведения
    context_contact = school_context_contact(school_menu)
    #руководитель учрж.
    context_led = school_led(school_menu)
    #Куратор
    context_curator = school_context_curators(school_menu)
    #Виды спорта
    context_sh_count = school_contex_count(name_school, df_school)
    #Объеденение
    context = (
            context_header+
            context_contact+
            context_led+
            context_curator+
            context_sh_count
            )
    return context


def mean_school_kpi(message, school_menu:int):
    df_today = school_mean_sport(school_menu)
    df_past = school_mean_sport_past(school_menu)
    # Объединение таблиц для создания общего DataFrame
    df = pd.merge(df_past, df_today, on='Вид спорта', suffixes=('_past', '_today'))
    image_name = get_school_kpi(message, df)
    with open(image_name, 'rb') as phote:
        bot.send_photo(message.chat.id, phote)
    os.remove(image_name)
    return


def print_school(message, sport_menu:str):
    msg = bot.send_message(message.chat.id, '🚴‍♂️ Обрабатываю Ваш запрос ...')
    school_menu = sport_menu.replace('sсhool_menu_', '')
    school_menu = int(school_menu)
    add_loger(message, 'sсhool_menu', school_menu)
    try:
        context_school_sport = school_mean_reg(school_menu)
        bot.send_message(message.chat.id, context_school_sport, parse_mode='HTML')
        mean_school_kpi(message, school_menu)
        bot.delete_message(message.chat.id, msg.message_id)
        upd_loger_finishhim(message, 'sсhool_menu', school_menu)
        return
    except Exception as e:
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, f"Что-то пошло не так. Попробуйте снова. \nКод ошибки:\n{e}")
        upd_loger_finishhim(message, 'sсhool_menu', school_menu, e)
        return