from database.conn_db import postgresql_to_dataframe, postgresql_to_data, postgresql_to_check
from database.conn_db import copy_from_file


def fk5_to_bd(df):
    col_bd = ['id_firm',
          'id_sport',
          'total_sport',
          'rank_r',
          'rank_r_kms',
          'rank_r_1r',
          'rank_r_other',
          'rank_z',
          'rank_z_zms',
          'rank_z_msmk',
          'rank_z_ms',
          'rank_z_grm',
          'reporting_year']
    copy_from_file(df, 'fk_order_r5', col_bd)


#Запросы к БД
def token_school():
    df =  postgresql_to_dataframe(
        """
        select
        id_firm,
        name_short,
        name_altarnative 
        FROM supra.dict_firm
        ;
        """, ['id', 'name_short', 'name_altarnative'])
    return df.sort_values('name_short', ascending=True)

def token_sport():
    df =  postgresql_to_dataframe(
        """
        select
        id_sport,
        name_sport
        FROM supra.dict_sport dts 
        ;
        """, ['id', 'Вид спорта'])
    return df