from database.conn_db import postgresql_to_dataframe, copy_from_file, postgresql_to_data

col_bd = ['id_ogrn', 'id_sport', 'name_fed', 'leader_job', 
          'leader_name', 'leader_birth', 'leader_contact',
          'fed_addres', 'fed_contact', 'fed_website', 
          'fed_email', 'fed_rd', 'fed_date_rd', 
          'fed_date_text', 'fed_date_finesh']

def fed_add_to_bd(df):
    copy_from_file(df, 'fed_order', col_bd)
    return


def token_sport():
    df =  postgresql_to_dataframe(
        """
        SELECT
        id_sport,
        name_sport
        FROM supra.dict_sport dts 
        ;
        """, ['id', 'name_sport'])
    return df


def fed_to_id_tuple():
    df =  postgresql_to_dataframe(
        """
        SELECT 
        id
        FROM supra.fed_order
        WHERE archiv_data = '0'
        ;
        """, ['id'])
    df_tuple = tuple(df['id'])
    return df_tuple


def arhiv_id_fed(df_tuple:[int])-> (int):
    ids = ', '.join(map(str, df_tuple))
    query = f"""
        UPDATE supra.fed_order   
        SET archiv_data = '1' 
        WHERE id IN ({ids});
    """
    postgresql_to_data(query)