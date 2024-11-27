import numpy as np
#Mod
from database.conn_db import postgresql_to_dataframe, postgresql_to_data

def firm_report():
	colum_name = ['Учреждение', 'Общая численность', 'НП', 'ТЭ', 
	'СС', 'ВСМ', 'Гос работа', 'Гос задание']
	df =  postgresql_to_dataframe(
		"""
		SELECT
		df.name_altarnative,
		sum(gos.total_sport) as total_sport,
		sum(gos.np) AS np,
		sum(gos.te) AS te,
		sum(gos.cc) AS cc,
		sum(gos.vcm) AS vcm,
		sum(gos.gos_work) AS gos_work,
		gos.name_file 
		FROM supra.gos_order gos
		INNER JOIN dict_firm df ON gos.id_firm = df.id_firm 
		WHERE gos.archiv_data = '0'
		AND created_at = (
		SELECT 
		created_at 
		FROM supra.gos_order
		WHERE archiv_data = '0'
		GROUP BY created_at ORDER BY created_at DESC LIMIT 1
		)
		GROUP BY name_altarnative, name_file ORDER BY total_sport DESC 
		;
      	""", colum_name)
	df = df.astype({"Общая численность": int})
	df.index = np.arange(1, len(df) + 1)
	df.loc[0] = ['ИТОГО', df['Общая численность'].sum(), df['НП'].sum(), 
             df['ТЭ'].sum(), df['СС'].sum(), df['ВСМ'].sum(),
            df['Гос работа'].sum(), 'Гос задание'] 
	return df


def sport_report():
	colum_name = ['Вид спорта', 'Общая численность', 'НП', 'ТЭ', 
	'СС', 'ВСМ', 'Гос работа', 'Гос задание']
	df =  postgresql_to_dataframe(
		"""
		SELECT
		ds.name_sport, 
		sum(gos.total_sport) as total_sport,
		sum(gos.np) AS np,
		sum(gos.te) AS te,
		sum(gos.cc) AS cc,
		sum(gos.vcm) AS vcm,
		sum(gos.gos_work) AS gos_work,
		gos.name_file 
		FROM supra.gos_order gos
		INNER JOIN dict_sport ds ON gos.id_sport = ds.id_sport 
		WHERE gos.archiv_data = '0'
		AND created_at = (
		SELECT 
		created_at 
		FROM supra.gos_order
		WHERE archiv_data = '0'
		GROUP BY created_at ORDER BY created_at DESC LIMIT 1
		)
		GROUP BY name_sport, name_file ORDER BY name_sport
		;
		""", colum_name)
	df = df.astype({"Общая численность": int})
	df.index = np.arange(1, len(df) + 1)
	df.loc[0] = ['ИТОГО', df['Общая численность'].sum(), df['НП'].sum(), 
             df['ТЭ'].sum(), df['СС'].sum(), df['ВСМ'].sum(),
            df['Гос работа'].sum(), 'Гос задание'] 
	return df


def global_report():
	colum_name = ['Учреждение', 'Вид спорта', 'Общая численность', 
	'НП1', 'НП2', 'НП3', 'НП4', 'НП', 'НПпк', 
	'ТЭ1', 'ТЭ2', 'ТЭ3', 'ТЭ4' , 'ТЭ5', 'ТЭ', 'ТЭпк',
	'СС1', 'СС2', 'СС3', 'СС', 'ССпк',
	'ВСМ', 'ВСМпк',
	'Гос работа', 'Гос задание', 'Дата актуализации'
	]
	df =  postgresql_to_dataframe(
		"""
		SELECT
		df.name_altarnative,
		ds.name_sport,
		gos.total_sport,
		gos.np1,
		gos.np2,
		gos.np3,
		gos.np4,
		gos.np,
		gos.np_pk,
		gos.te1,
		gos.te2,
		gos.te3,
		gos.te4,
		gos.te5,
		gos.te,
		gos.te_pk,
		gos.cc1,
		gos.cc2,
		gos.cc3,
		gos.cc,
		gos.cc_pk,
		gos.vcm,
		gos.vcm_pk,
		gos.gos_work,
		gos.name_file,
		gos.created_at 
		FROM supra.gos_order gos
		INNER JOIN supra.dict_firm df ON gos.id_firm = df.id_firm 
		INNER JOIN supra.dict_sport ds ON gos.id_sport = ds.id_sport 
		WHERE gos.archiv_data = '0'
		AND created_at = 
		(
		SELECT 
		created_at 
		FROM supra.gos_order
		WHERE archiv_data = '0'
		GROUP BY created_at ORDER BY created_at DESC LIMIT 1
		)
		;
      	""", colum_name)

	return df

def kpi_gos_mean():
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
		gos.name_file 
		FROM supra.gos_order gos 
		WHERE archiv_data = '0'
		AND name_file IN 
		(
		SELECT name_file
		FROM supra.gos_order
		GROUP BY name_file
		ORDER BY MAX(created_at) DESC
		LIMIT 8
		)
		OR name_file  = 'ГЗ 1 сентября 2022'
		GROUP BY gos.name_file, gos.created_at ORDER BY gos.created_at 
		;""", colum_name)
	return df


