#Mod
from database.conn_db import postgresql_to_dataframe, postgresql_to_data, postgresql_to_check



def load_menu_attribut_two(message, menu_function, attribut_one):
	menu_attribut = postgresql_to_check(
		"""
		SELECT
		attribute_name2
		FROM supra.user_log_analize
		where id_user = %s
		and menu_function = '%s'
		and attribute_name1 = '%s'
		and finish_check = '0'
		"""%(message.chat.id, menu_function, attribut_one))
	return menu_attribut