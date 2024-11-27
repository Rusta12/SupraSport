from database.conn_db import postgresql_to_dataframe, copy_from_file, postgresql_to_data


def df_sport():
    df =  postgresql_to_dataframe(
        """
        SELECT
        id_sport,
        name_sport,
        status_sport,
        category_sport,
        archiv_sport
        FROM supra.dict_sport dts 
        ;
        """, [
            'id_sport',
            'Наименование вида спорта',
            'status_sport',
            'category_sport',
            'archiv_sport'])
    return df


def upd_dict_sport(id_old:int, id_new:int, razdel:str):
    postgresql_to_data(
        f"""
        UPDATE supra.dict_sport 
        SET id_sport = {id_new},
            razdel_sport = '{razdel}'
        WHERE id_sport = {id_old}
        """
    )

def insert_dict_sport(id_sport:int, name_sport:str, razdel:str, status_sport=None,category_sport=None):
    postgresql_to_data(
        f"""
        INSERT INTO supra.dict_sport 
        (id_sport, name_sport, razdel_sport, status_sport,category_sport)
        VALUES
        ({id_sport},'{name_sport}','{razdel}','{status_sport}', '{category_sport}')
        """
    )