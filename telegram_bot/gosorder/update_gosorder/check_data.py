import pandas as pd
#Mod
import gosorder.update_gosorder.reference as rf



def check_name_file(path_file:str):
	path_file = path_file.replace(r"Свод ", "")
	path_file = path_file.replace(r".xlsx", "")
	path_file = path_file.replace(r"./gosorder/update_gosorder/Temp/", "")
	id_tuple = rf.name_file_to_id_tuple(f'%{path_file}%')
	return id_tuple


def arhiv_data(df_tuple:(int))-> (int):
	rf.arhiv_id_gos(df_tuple)


