import pandas as pd
import os



def path_to_file(path):
	files_list = os.listdir(f".{path}")
	df_files = pd.DataFrame(files_list, columns=["Name"])
	df_files = df_files.replace(r".xlsm", "",  regex=True)
	df_files = df_files.replace(r"МКСШОР ", "",  regex=True)
	df_files = df_files.replace(r"Московская академия парусного и гребных видов спорта", "Парус и гребля",  regex=True)
	df_files = df_files.replace(r"Московская академия велосипедного спорта", "Велосипед",  regex=True)
	df_files = df_files.replace(r"Московская академия фигурного катания на коньках", "Фигурное катание",  regex=True)
	df_files = df_files.replace(r"Московская волейбольная академия", "Волейбол",  regex=True)
	df_files = df_files.replace(r"Московская академия хоккея", "Хоккей",  regex=True)
	df_files = df_files.replace(r"Московская академия зимних видов спорта", "Зима",  regex=True)
	df_files = df_files.replace(r"Московская академия плавания", "Плавание",  regex=True)
	df_files = df_files.replace(r"Московская академия современного пятиборья", "Пятиборье",  regex=True)
	df_files = df_files.replace(r"Московская комплексная спортивная школа Зеленоград", "Зеленоград",  regex=True)
	df_files = df_files.replace(r"Московская академия лыжных гонок и биатлона", "Лыжи",  regex=True)
	df_files = df_files.replace(r"Московская академия регби", "Регби",  regex=True)
	df_files = df_files.replace(r"Московская футбольная академия", "Футбол",  regex=True)
	df_files = df_files.replace(r"Самбо-70", "Самбо70",  regex=True)
	df_files = df_files.replace(r"КФКС Спарта", "Спарта",  regex=True)
	df_files = df_files.replace(r"Московская теннисная академия", "Теннис",  regex=True)
	df_files = df_files.replace(r"00 Юность Москвы 2022", "ЮМ",  regex=True)
	df_files = df_files.replace(r"Спортивный интернат Чертаново", "Чертаново",  regex=True)
	df_files = df_files.replace(r"Москва-98", "М98",  regex=True)
	df_files = df_files.replace(r"Московская гандбольная академия", "Гандбол",  regex=True)
	df_files = df_files.replace(r"00 МГФСО 2022", "МГФСО",  regex=True)
	df_files = df_files.replace(r"ЮГ", "Юг",  regex=True)
	df_files = df_files.replace(r"Московская_горнолыжная_академия_", "Горные лыжи",  regex=True)
	df_files = df_files.replace(r"00МБА2022", "Баскетбол",  regex=True)
	for x in range(len(files_list)):
	    old_name = f".{path}{files_list[x]}"
	    new_name = f".{path}{df_files.loc[x, 'Name']}.xlsm"
	    os.rename(old_name, new_name)   
	return print('Файлы перемейнованы.', list(df_files['Name']))


def path_to_file_altarnative(path):
	files_list = os.listdir(f".{path}")
	df_files = pd.DataFrame(files_list, columns=["Name"])
	df_files = df_files.replace(r".xlsm", "",  regex=True)
	for x in range(len(files_list)):
	    old_name = f".{path}{files_list[x]}"
	    new_name = f".{path}{df_files.loc[x, 'Name']}.xlsm"
	    os.rename(old_name, new_name)   
	return print('Файлы перемейнованы.', list(df_files['Name']))