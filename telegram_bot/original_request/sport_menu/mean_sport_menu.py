from config import bot
from telebot import types
from datetime import datetime
import os
import pandas as pd
#Mod

#Стикер АО
#CAACAgIAAxkBAAEIZQ5kJrjRmisxkyIT5gKjzmCr6-xkigACFwADajzGERemoBXXfe-4LwQ

from original_request.reference_reg import sport_mean_school, sport_name_sport, sport_mean_fed, sport_mean_school_past
from original_request.reference_reg import sport_rank_statistics, sport_mean_fk5_r9
from database.attributs import upd_loger_finishhim, add_loger
from original_request.sport_menu.kpi_sport_menu import get_sport_kpi


def sport_federation_contex(df, name_sport:str):
	today = datetime.today().date()
	if df.shape[0] != 0:
		fed_name = df.loc[0, 'name_fed']
		name_job = df.loc[0, 'leader_job']
		fio_name = df.loc[0, 'leader_name']
		fio_contact = df.loc[0, 'leader_contact']
		name_rp = df.loc[0, 'fed_rd']
		name_data = df.loc[0, 'fed_date_rd']
		name_data_str = name_data.strftime('%d.%m.%Y')
		name_period = df.loc[0, 'fed_date_text']
		name_finish = df.loc[0, 'fed_date_finesh']
		name_finish_str = name_finish.strftime('%d.%m.%Y')
		contakt_email = df.loc[0, 'fed_email']
		contakt_url = df.loc[0, 'fed_website']
		contakt_tel = df.loc[0, 'fed_contact']
		ogrn = df.loc[0, 'id_ogrn']
		if name_finish > today:
			FdName = f'На территории города Москвы развитием и популяризацией вида спорта {name_sport.lower()} ' \
					f'занимается {fed_name} (далее – Федерация). \n<b>{name_job} – {fio_name}.</b>\n'\
					f'<b>Контактный телефон руководителя:</b> {fio_contact}\n'
			DataFd = f'На основании распоряжения о государственной аккредитации ' \
					f'региональных спортивных федераций № {name_rp} от {name_data_str} г. ' \
					f'Федерация аккредитована сроком на {name_period}. Срок действия аккредитации ' \
					f'Федерации до {name_finish_str} г.\n\n'
			ConFd = f"<b>Почта:</b> {contakt_email}\n"\
					f"<b>Сайт:</b> {contakt_url}\n"\
					f"{contakt_tel}\n"
			ogrn_f = f"ОГРН: {ogrn}\n\n"
			context = FdName+DataFd+ConFd+ogrn_f
			return context
		else:
			FdName = f'Внимание ⚠️ закончилась аккредитация у Федерации ({fed_name}) аккредитация была до {name_finish_str} г.❌\n'
			DataFd = f'На основании распоряжения о государственной аккредитации ' \
					f'региональных спортивных федераций № {name_rp} от {name_data_str} г. \n\n'
			ConFd = f"<b>Почта:</b> {contakt_email}\n"\
					f"<b>Сайт:</b> {contakt_url}\n"\
					f"{contakt_tel}\n"
			ogrn_f = f"ОГРН: {ogrn}\n\n"
			context = FdName+DataFd+ConFd+ogrn_f
			return context
	else:
		context = f'На территории города Москвы отсуствует аккредитованая федерация по виду спорта {name_sport.lower()}\n\n'
		return context

def sport_contex_count(name_sport:str, df_school):
	if df_school.shape[0] > 1:
		count_sh = df_school.shape[0]
		list_sh = df_school['Учреждение'].to_list()
		name_sh = '\n- '.join(list_sh)
		name_sh = f'\n- {name_sh}'
		context = "В системе Москомспорта дополнительная образовательная программа спортивной подготовки "\
							f"по виду спорта «{name_sport.lower()}» реализуется"\
							f" в <b>{count_sh}</b> учреждениях."\
							f"\n{name_sh}"
		return context

	elif df_school.shape[0] == 1:
		count_sh = df_school.shape[0]
		list_sh = df_school.loc[0 , 'Учреждение']
		name_sh = f'\n- {list_sh}'
		context = "В системе Москомспорта дополнительная образовательная программа спортивной подготовки "\
							f"по виду спорта «{name_sport.lower()}» реализуется"\
							f" в {name_sh}."
		return context

	else:
		context = f"В системе Москомспорта дополнительная образовательная программа спортивной подготовки "\
							f"по виду спорта «{name_sport.lower()}» не реализуется"
		return context

def sport_contex_sum(df_school):
	if df_school.shape[0] != 0:
		SumAll = df_school['Общая численность'].sum()
		SumNp = df_school['НП'].sum()
		SumTe = df_school['ТЭ'].sum()
		SumSs = df_school['СС'].sum()
		SumVsm = df_school['ВСМ'].sum()
		SumGs = df_school['Гос работа'].sum()
		if df_school.shape[0] > 1:
			SumAll = '{:,}'.format(SumAll).replace(',', ' ')
			SumAll = f'\n\nВ указанных учреждениях занимаются <b>{SumAll} чел.</b>, из них:'
		elif df_school.shape[0] == 1:
			SumAll = f'\n\nВ указанном учреждении занимается <b>{SumAll} чел.</b>, из них:'

		if SumNp != 0:
			SumNp = '{:,}'.format(SumNp).replace(',', ' ')
			SumNp = f'\n– этап начальной подготовки – <b>{SumNp} чел.</b>\n'
		else:
			SumNp =''
		if SumTe != 0:
			SumTe = '{:,}'.format(SumTe).replace(',', ' ')
			SumTe = f'– учебно-тренировочный этап – <b>{SumTe} чел.</b>\n'
		else:
			SumTe = ''
		if SumSs != 0:
			SumSs = f'– этап совершенствования спортивного мастерства – <b>{SumSs} чел.</b>\n'
		else:
			SumSs =''
		if SumVsm != 0:
			SumVsm = f'– этап высшего спортивного мастерства – <b>{SumVsm} чел.</b>\n'
		else:
			SumVsm = ''
		if SumGs != 0:
			SumGs = f'– спортсмены, трудоустроенные в учреждении – <b>{SumGs} чел.</b>'
		else:
			SumGs = ''
	else:
		SumAll = ''
		SumNp = ''
		SumTe = ''
		SumSs = ''
		SumVsm = ''
		SumGs = ''
	contex = SumAll+SumNp+SumTe+SumSs+SumVsm+SumGs
	return contex

def sport_rank_stat(df):
	if df.loc[0,'total_sport'] != None:
		Total = df.loc[0, 'total_sport']
		Other = df.loc[0, 'total_other']
		r1 = df.loc[0, 'total_1r']
		kms = df.loc[0, 'total_kms']
		ms = df.loc[0, 'total_ms']
		msmk = df.loc[0, 'total_msmk']
		zms = df.loc[0, 'total_zms']
		grm = df.loc[0, 'total_grm']
		#добавление текста
		if Total != 0:
			Total = '{:,}'.format(Total).replace(',', ' ')
			Total = f'\n\nСпортивные разряды имеют <b>{Total} чел.,</b> из них:'
		else:
			Total = ''
		#Общие
		if Other != 0:
			Other = '{:,}'.format(Other).replace(',', ' ')
			Other = f'\n– массовые разряды – <b>{Other} чел.</b>;'
		else:
			Other = ''
		#Первый
		if r1 != 0:
			r1 = f'\n– 1 разряд – <b>{r1} чел.</b>;'
		else:
			r1 = ''
		#КМС
		if kms != 0:
			kms = f'\n– КМС – <b>{kms} чел.</b>'
		else:
			kms = ''
		#MC
		if ms != 0:
			ms = f'\n– МС – <b>{ms} чел.</b>'
		else:
			ms = ''
		#МСМК
		if msmk != 0:
			msmk = f'\n– МСМК – <b>{msmk} чел.</b>'
		else:
			msmk = ''
		#ЗМС
		if zms != 0:
			zms = f'\n– ЗМС – <b>{zms} чел.</b>'
		else:
			zms = ''
		#ГРМ
		if grm != 0:
			grm = f'\n– Гроссмейстер – <b>{grm} чел.</b>'
		else:
			grm = ''
		contex = Total+Other+r1+kms+ms+msmk+zms+grm
		return contex 
	else:
		contex =''
		return contex

def sport_fk_r9(df):
	if df.loc[0,'trainers'] != None:
		trainers = df.loc[0, 'trainers']
		ztr = df.loc[0, 'ztr']
		#Общие
		if trainers == 1:
			trainers = f'\n\nРаботу с обучающимися проводит <b>один тренер-преподаватель</b> '
		elif trainers > 1 and trainers < 5:
			trainers = f'\n\nРаботу с обучающимися проводят <b>{trainers} тренера-преподавателя</b> '
		elif trainers > 4:
			trainers = f'\n\nРаботу с обучающимися проводят <b>{trainers} тренеров-преподавателей</b> '
		if ztr == 1:
			ztr = f'(из них <b>один тренер-преподаватель</b> имеет почетное звание «Заслуженный тренер России»).'
		elif ztr == 2:
			ztr = f'(из них <b>двое тренеров-преподавателей</b> имеют почетное звание «Заслуженный тренер России»).'
		elif ztr > 2 and ztr < 5:
			ztr = f'(из них <b>{ztr} тренера-преподавателя</b> имеют почетное звание «Заслуженный тренер России»).'
		elif ztr > 4:
			ztr = f'(из них <b>{ztr}</b> человек имеют почетное звание «Заслуженный тренер России»).'
		elif ztr == 0:
			ztr = ''
		contex = trainers+ztr
		return contex 
	else:
		contex =''
		return contex


def sport_team_context(sport_id:id):
	context = f"\n\n<em>Тут будет информация по сборной команде пока в проекте!</em>"
	return context

def sport_events_context(sport_id:id):
	context = f"\n\n<em>Тут будет информация по ЕКП пока в проекте!</em>"
	return context

def sport_mean_reg(sport_id:int):
	#Загрузска данных
	name_sport = sport_name_sport(sport_id)
	df_school = sport_mean_school(sport_id)
	df_fed = sport_mean_fed(sport_id)
	df_sport_rank = sport_rank_statistics(sport_id)
	df_fk5_r9 = sport_mean_fk5_r9(sport_id)
	#Загаловок
	context_header = f"Информационная справка по виду спорта <b>{name_sport.lower()}</b>\n\n"\
	#Федерация
	context_federation = sport_federation_contex(df_fed, name_sport)
	#Список школ
	context_sh_count = sport_contex_count(name_sport, df_school)
	#Суммы по занимающимся
	context_sh_sum = sport_contex_sum(df_school)
	#Стат отчет 5-ФК
	context_sport_rank = sport_rank_stat(df_sport_rank)
	context_fk_9_sum = sport_fk_r9(df_fk5_r9)
	#Сборники
	#contexе_team_sum = sport_team_context(sport_id)
	#Мероприятия
	#contexе_event_sum = sport_events_context(sport_id)
	#Объеденение
	context = (
		context_header+
		context_federation+
		context_sh_count+
		context_sh_sum+
		context_sport_rank+
		context_fk_9_sum
		)

	return context

def mean_sport_kpi(message, sport_id:int):
	df_today = sport_mean_school(sport_id)
	df_past = sport_mean_school_past(sport_id)
	# Объединение таблиц для создания общего DataFrame
	df = pd.merge(df_past, df_today, on='Учреждение', suffixes=('_past', '_today'))
	try:
		image_name = get_sport_kpi(message, df)
		with open(image_name, 'rb') as phote:
			bot.send_photo(message.chat.id, phote)
		os.remove(image_name)
		return
	except:
		return


def print_sport(message, sport_menu:str):
	msg = bot.send_message(message.chat.id, '🚴‍♂️ Обрабатываю Ваш запрос ...')
	sport_menu = sport_menu.replace('sport_menu_', '')
	sport_id = int(sport_menu)
	add_loger(message, 'sport_menu', sport_id)
	try:
		context_school_sport = sport_mean_reg(sport_id)
		bot.send_message(message.chat.id, context_school_sport, parse_mode='HTML')
		#mean_sport_kpi(message, sport_id)
		bot.delete_message(message.chat.id, msg.message_id)
		upd_loger_finishhim(message, 'sport_menu', sport_id)
		return
	except Exception as e:
		bot.delete_message(message.chat.id, msg.message_id)
		bot.send_message(message.chat.id, f"Что-то пошло не так. Попробуйте снова. \nКод ошибки:\n{e}")
		upd_loger_finishhim(message, 'sport_menu', sport_id, e)


