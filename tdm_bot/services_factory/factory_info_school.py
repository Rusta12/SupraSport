from datetime import datetime
import os
import pandas as pd

from database.select_school import school_name_school, school_mean_sport, school_mean_curator
from database.select_school import school_rank_statistics, school_stat_trainer
from database.select_school import school_mean_firm, school_led_firm


def school_context_contact(school_menu:int):
    df = school_mean_firm(school_menu)
    name_full = df.loc[0, 'name_full']
    contakt_email = df.loc[0, 'contakt_email']
    contakt_tel = df.loc[0, 'contakt_tel']
    contakt_url = df.loc[0, 'contakt_url']
    firm_url = df.loc[0, 'firm_url']
    ogrn = df.loc[0, 'ogrn']
    context = f"[url={firm_url}]{name_full}[/url]\n"\
            f"ОГРН: {ogrn}\n"\
            f"[b]Почта:[/b] {contakt_email}\n"\
            f"[b]Сайт:[/b] {contakt_url}\n"\
            f"[b]Телефоны:[/b] {contakt_tel}\n\n"
    return context

def school_led(school_menu:int):
    df = school_led_firm(school_menu)
    led_job = df.loc[0, 'name_job']
    led_name = df.loc[0, 'name_led']
    led_cotakt = df.loc[0, 'led_cotakt']
    led_email = df.loc[0, 'led_mail']
    context = f"[b]{led_job.title()}[/b]\n{led_name}\n{led_cotakt}\n{led_email}\n\n"
    return context


def school_context_curators(school_menu:int):
	df = school_mean_curator(school_menu)
	name_curator = df.loc[0, 'name_curator']
	contakt_tel = df.loc[0, 'contakt_tel']
	contakt_email = df.loc[0, 'contakt_email']
	context = f'[b]Куратор Спортивного управления:[/b]\n{name_curator}, \n{contakt_tel}\n{contakt_email}\n\n'
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


def school_fk_r5(df):
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
		Total = '{:,}'.format(Total).replace(',', ' ')
		Total = f'\n\nСпортивные разряды имеют [b]{Total} чел.,[/b] из них:'
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

def school_fk_trainer(df):
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


def school_mean_reg(sport_menu:str):
    school_menu = sport_menu.replace('sсhool_menu_', '')
    school_menu = int(school_menu)
    #Загрузска данных
    name_school = school_name_school(school_menu)
    df_school = school_mean_sport(school_menu)
    df_school_rank= school_rank_statistics(school_menu)
    df_trainer = school_stat_trainer(school_menu)
    #Загаловок
    context_header = f"Информационная справка по учреждению: \n[b]{name_school}[/b]\n\n"
    #Общие сведения
    context_contact = school_context_contact(school_menu)
    #руководитель учрж.
    context_led = school_led(school_menu)
    #Куратор
    context_curator = school_context_curators(school_menu)
    #Виды спорта
    context_sh_count = school_contex_count(name_school, df_school)
    # Стат отчет 5-ФК Разряды Тренеры
    context_school_rank_sum = school_fk_r5(df_school_rank)
    context_trainer = school_fk_trainer(df_trainer)
    #Объеденение
    context = (
            context_header+
            context_contact+
            context_led+
            context_curator+
            context_sh_count+
            context_school_rank_sum+
            context_trainer+'\n\n'
            )
    return context