#Mod
from database.conn_db import postgresql_to_dataframe, postgresql_to_data, postgresql_to_check



#проверка пользователя в БД
def chek_user_count(user_id: int):
	check_user_access = postgresql_to_dataframe(
		"""
		SELECT count(*) 
		FROM supra.user_protection
		WHERE id_user = %s
		AND arhiv = '0'
		;
		"""
		%(user_id), ['user_id'])
	check_user_access = tuple(check_user_access['user_id'])
	return check_user_access[0]


#внесения пользователя с ролью 0
def add_user_bd(user_id: int, name: str, tg_name:str='None'):
	postgresql_to_data(
		"""
		INSERT INTO supra.user_protection (id_user, username, tg_name, id_role_access)
		VALUES (%s, '%s', '%s', 0)
		;
		"""
		%(user_id, name, tg_name))

#вывод информации о пользователе в профиль
def chek_user_profile(user_id: int):
	column_names = ['id_role_access', 'id_user', 'username',
	'email', 'phone', 'arhiv']
	check_user_access = postgresql_to_dataframe(
		"""
		SELECT
		id_role_access,
		id_user,
		username,
		email,
		phone,
		arhiv
		FROM supra.user_protection
		WHERE id_user = %s
		;
		"""
		%(user_id), column_names)
	
	return check_user_access


def chek_user_access(user_id: int):
	check_user_access = postgresql_to_check(
		"""
		SELECT
		id_role_access
		FROM supra.user_protection
		where id_user = %s
		;
		"""
		%(user_id))
	return check_user_access
