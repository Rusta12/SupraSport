from datetime import datetime
import os
import pandas as pd
#Mod
from database.select_sport import sport_mean_school, sport_name_sport, sport_mean_fed
from database.select_sport import sport_rank_statistics, sport_stat_trainer



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
					f'занимается {fed_name} (далее – Федерация). \n[b]{name_job} – {fio_name}.[/b]\n'\
					f'[b]Контактный телефон руководителя:[/b] {fio_contact}\n'
			DataFd = f'На основании распоряжения о государственной аккредитации ' \
					f'региональных спортивных федераций № {name_rp} от {name_data_str} г. ' \
					f'Федерация аккредитована сроком на {name_period}. Срок действия аккредитации ' \
					f'Федерации до {name_finish_str} г.\n\n'
			ConFd = f"[b]Почта:[/b] {contakt_email}\n"\
					f"[b]Сайт:[/b] [url]{contakt_url}[/url]\n"\
					f"{contakt_tel}\n"
			ogrn_f = f"ОГРН: {ogrn}\n\n"
			context = FdName+DataFd+ConFd+ogrn_f
			return context
		else:
			FdName = f'Внимание ⚠️ закончилась аккредитация у Федерации ({fed_name}) аккредитация была до {name_finish_str} г.❌\n'
			DataFd = f'На основании распоряжения о государственной аккредитации ' \
					f'региональных спортивных федераций № {name_rp} от {name_data_str} г. \n\n'
			ConFd = f"[b]Почта:[/b] {contakt_email}\n"\
					f"[b]Сайт:[/b] [url]{contakt_url}[/url]\n"\
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
							f" в [b]{count_sh}[/b] учреждениях."\
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
			SumAll = f'\n\nВ указанных учреждениях занимаются [b]{SumAll} чел.[/b], из них:'
		elif df_school.shape[0] == 1:
			SumAll = f'\n\nВ указанном учреждении занимается [b]{SumAll} чел.[/b], из них:'

		if SumNp != 0:
			SumNp = '{:,}'.format(SumNp).replace(',', ' ')
			SumNp = f'\n– этап начальной подготовки – [b]{SumNp} чел.[/b]\n'
		else:
			SumNp =''
		if SumTe != 0:
			SumTe = '{:,}'.format(SumTe).replace(',', ' ')
			SumTe = f'– учебно-тренировочный этап – [b]{SumTe} чел.[/b]\n'
		else:
			SumTe = ''
		if SumSs != 0:
			SumSs = f'– этап совершенствования спортивного мастерства – [b]{SumSs} чел.[/b]\n'
		else:
			SumSs =''
		if SumVsm != 0:
			SumVsm = f'– этап высшего спортивного мастерства – [b]{SumVsm} чел.[/b]\n'
		else:
			SumVsm = ''
		if SumGs != 0:
			SumGs = f'– спортсмены, трудоустроенные в учреждении – [b]{SumGs} чел.[/b]'
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
			Total = f'\n\nСпортивные разряды имеют [b]{Total} чел.,[/b] из них:'
		else:
			Total = ''
		#Общие
		if Other != 0:
			Other = '{:,}'.format(Other).replace(',', ' ')
			Other = f'\n– массовые разряды – [b]{Other} чел.[/b];'
		else:
			Other = ''
		#Первый
		if r1 != 0:
			r1 = f'\n– 1 разряд – [b]{r1} чел.[/b];'
		else:
			r1 = ''
		#КМС
		if kms != 0:
			kms = f'\n– КМС – [b]{kms} чел.[/b]'
		else:
			kms = ''
		#MC
		if ms != 0:
			ms = f'\n– МС – [b]{ms} чел.[/b]'
		else:
			ms = ''
		#МСМК
		if msmk != 0:
			msmk = f'\n– МСМК – [b]{msmk} чел.[/b]'
		else:
			msmk = ''
		#ЗМС
		if zms != 0:
			zms = f'\n– ЗМС – [b]{zms} чел.[/b]'
		else:
			zms = ''
		#ГРМ
		if grm != 0:
			grm = f'\n– Гроссмейстер – [b]{grm} чел.[/b]'
		else:
			grm = ''
		contex = Total+Other+r1+kms+ms+msmk+zms+grm
		return contex 
	else:
		contex =''
		return contex

def sport_fk_trainer(df):
	if df.loc[0,'trainers'] != None:
		trainers_count = df.loc[0, 'trainers']
		ztr_count = df.loc[0, 'ztr']
		age_to_35 = df.loc[0, 'age_to_35']
		age_36_to_64 = df.loc[0, 'age_36_to_64']
		age_64_to_old = df.loc[0, 'age_64_to_old']

		def plural_form(number, singular, few, many):
			if 11 <= number % 100 <= 19:
				return many
			rem = number % 10
			if rem == 1:
				return singular
			if 2 <= rem <= 4:
				return few
			return many

		#Общие количество
		trainer_word = plural_form(trainers_count,
								'тренер-преподаватель',
								'тренера-преподавателя',
								'тренеров-преподавателей')
		if trainers_count == 1:
			trainers_text = f'\n\nРаботу с обучающимися проводит [b]один {trainer_word}[/b] '
		else:
			trainers_text = f'\n\nРаботу с обучающимися проводят [b]{trainers_count} {trainer_word}[/b] '

		# --- Часть про заслуженных тренеров (было) ---
		if pd.isna(ztr_count) or ztr_count == 0:
			honored_text = ''
		else:
			honored_word = plural_form(ztr_count,
									'тренер-преподаватель',
									'тренера-преподавателя',
									'тренеров-преподавателей')
			if ztr_count == 1:
				honored_text = f'(из них [b]один {honored_word}[/b] имеет почетное звание «Заслуженный тренер России»).'
			elif 2 <= ztr_count <= 4:
				honored_text = f'(из них [b]{ztr_count} {honored_word}[/b] имеют почетное звание «Заслуженный тренер России»).'
			else:
				person_word = plural_form(ztr_count, 'человек', 'человека', 'человек')
				honored_text = f'(из них [b]{ztr_count} {person_word}[/b] имеют почетное звание «Заслуженный тренер России»).'

		#Возраста
		age_groups = [
				(age_to_35, 'до 35 лет'),
				(age_36_to_64, '36–64 года'),
				(age_64_to_old, 'старше 64 лет')
			]
		non_empty = [(cnt, label) for cnt, label in age_groups
					if not pd.isna(cnt) and cnt > 0]

		if not non_empty:
			age_text = ''
		else:
			# Формируем перечисление возрастных групп
			parts = []
			for cnt, label in non_empty:
				# Склоняем «человек» под каждое число
				people_word = plural_form(cnt, 'человек', 'человека', 'человек')
				parts.append(f'[b]{cnt}[/b] {people_word} {label}')

			if len(parts) == 1:
				age_text = f'\nВозрастной состав:\n– {parts[0]}.'
			elif len(parts) == 2:
				age_text = f'\nВозрастной состав:\n– {parts[0]};\n– {parts[1]}.'
			else:  # 3 части
				age_text = f'\nВозрастной состав:\n– {parts[0]};\n– {parts[1]};\n– {parts[2]}.'
		
		contex = trainers_text + honored_text + age_text
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

def sport_mean_reg(sport_menu:str):
	sport_menu = sport_menu.replace('sport_menu_', '')
	sport_id = int(sport_menu)
	#Загрузска данных
	name_sport = sport_name_sport(sport_id)
	df_school = sport_mean_school(sport_id)
	df_fed = sport_mean_fed(sport_id)
	df_sport_rank = sport_rank_statistics(sport_id)
	df_trainer = sport_stat_trainer(sport_id)
	#Загаловок
	context_header = f"Информационная справка по виду спорта [b]{name_sport.lower()}[/b]\n\n"\
	#Федерация
	context_federation = sport_federation_contex(df_fed, name_sport)
	#Список школ
	context_sh_count = sport_contex_count(name_sport, df_school)
	#Суммы по занимающимся
	context_sh_sum = sport_contex_sum(df_school)
	#Стат отчет 5-ФК
	context_sport_rank = sport_rank_stat(df_sport_rank)
	context_trainer = sport_fk_trainer(df_trainer)
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
		context_trainer+'\n\n'
		)

	return context