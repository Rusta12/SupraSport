from database.conn_db import postgresql_to_dataframe, postgresql_to_data

def firm():
    df =  postgresql_to_dataframe(
    	"""
		SELECT 
		id_firm,
		name_short 
		FROM supra.dict_firm   
		WHERE archiv_sport = '0'
		;
      	""", ['id_firm', 'name_short'])
    return df


def token_sport():
    df =  postgresql_to_dataframe(
    	"""
		SELECT 
		id_sport,
        token_sport
		FROM supra.dict_token_sport
		;
      	""", ['id_sport', 'Вид спорта'])
    return df


def name_file():
    df =  postgresql_to_dataframe(
    	"""
		SELECT 
		name_file 
		FROM supra.gos_order go2
		where archiv_data ='0'
		group by name_file 
		;
      	""", ['name_file'])
    return df


def name_file_and_date():
    df =  postgresql_to_dataframe(
    	"""
		SELECT 
		id, name_file, created_at 
		FROM supra.gos_order go2
		where archiv_data ='0'
		;
      	""", ['id', 'name_file', 'created_at'])
    return df


def name_file_to_id_tuple(name_file):
    df =  postgresql_to_dataframe(
    	"""
		SELECT 
		id
		FROM supra.gos_order go2 
		WHERE archiv_data = '0'
		AND name_file like '%s'
		;
      	""" %(name_file), ['id'])
    df_tuple = tuple(df['id'])
    return df_tuple


def arhiv_id_gos(df_tuple:[int])-> (int):
	ids = ', '.join(map(str, df_tuple))
	query = f"""
		UPDATE supra.gos_order	
		SET archiv_data = '1' 
		WHERE id IN ({ids});
		"""
	postgresql_to_data(query)

def total_gos_mean():
	colum_name = ['Общий', 'НП', 'ТЭ', 'СС', 'ВСМ', 'Гос работа', 'Гос задание']
	df =  postgresql_to_dataframe(
		"""
		SELECT
		sum(gos.total_sport) AS total_sport,
		sum(gos.np) AS np,
		sum(gos.te) AS te,
		sum(gos.cc) AS cc,
		sum(gos.vcm) AS vcm,
		sum(gos.gos_work) AS gos_work,
		gos.name_file as name_file 
		FROM supra.gos_order gos 
		WHERE archiv_data = '0'
		AND created_at = 
		(
		SELECT 
		created_at 
		FROM supra.gos_order
		WHERE archiv_data = '0'
		GROUP BY created_at ORDER BY created_at DESC LIMIT 1
		)
		GROUP BY name_file
		;""", colum_name)
	return df