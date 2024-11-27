#Mod
from database.conn_db import postgresql_to_dataframe, postgresql_to_data, postgresql_to_check



def add_user_analaze(message, menu_function: str, attribute_name_one:str):
	postgresql_to_data(
		"""
		INSERT INTO supra.user_log_analize (id_user, menu_function, attribute_name1)
		VALUES (%s, '%s', '%s')
		;
		"""
		%(message.chat.id, menu_function, attribute_name_one))


def check_user_analaze(message, menu_function:str):
	check_user = postgresql_to_check(
		"""
		SELECT COUNT(*) 
		FROM supra.user_log_analize
		WHERE id_user = %s
		and menu_function = '%s'
		and finish_check = '0'
		;
		"""
		%(message.chat.id, menu_function))
	return check_user


def upd_user_attribute_name_one(message, menu_function: str, attribute_name_one: str):
	postgresql_to_data(
		"""
		UPDATE supra.user_log_analize 
		SET attribute_name1 = '%s'
		WHERE id_user = %s
		and menu_function = '%s'
		and finish_check = '0'
		;
		"""
		%(attribute_name_one, message.chat.id, menu_function))

def upd_user_attribute_name_two(message, menu_function: str, attribute_name_two: str):
	postgresql_to_data(
		"""
		UPDATE supra.user_log_analize 
		SET attribute_name2 = '%s'
		WHERE id_user = %s
		and menu_function = '%s'
		and finish_check = '0'
		;
		"""
		%(attribute_name_two, message.chat.id, menu_function))

def upd_user_attribute_name_three(message, menu_function: str, attribute_name_three: str):
	postgresql_to_data(
		"""
		UPDATE supra.user_log_analize 
		SET attribute_name3 = '%s'
		WHERE id_user = %s
		and menu_function = '%s'
		and finish_check = '0'
		;
		"""
		%(attribute_name_three, message.chat.id, menu_function))


def upd_loger_finishhim(message, menu_function: str, attribute_name_one: str, fatality='Successfully'):
	postgresql_to_data(
		"""
		UPDATE supra.user_log_analize
		SET finish_check = '1',
		attribute_name3 = '%s'
		WHERE id_user = %s
		and menu_function = '%s'
		and attribute_name1 = '%s'
		and finish_check = '0'
		;
		"""
		%(fatality, message.chat.id, menu_function, attribute_name_one))


def add_loger(message, menu_function: str, attribute_name_one:str='0'):
	check_user = check_user_analaze(message, menu_function)
	if check_user == 0:
		add_user_analaze(message, menu_function, attribute_name_one)
	else:
		pass


def upd_loger_attribute_one(message, menu_function: str, attribute_name_one: str):
	check_user = check_user_analaze(message, menu_function, attribute_name_one)
	if check_user != 0:
		upd_user_attribute_name_one(message, menu_function, attribute_name_one)
	else:
		pass


