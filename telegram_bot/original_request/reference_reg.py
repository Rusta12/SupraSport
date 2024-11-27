from database.conn_db import postgresql_to_dataframe

def sport_token():
    column_names = ['token_name', 'menu', 'id', 'correct_name']
    df = postgresql_to_dataframe(
        """
        SELECT token_name,menu,id,correct_name
        FROM supra.union_token_sport
        ;
        """, column_names)
    df['id'] = df['id'].astype(str)
    df['menu'] = df['menu'] + '_' + df['id']
    df['token_name'] = df['token_name'].str.lower()

    return df


def sport_name_sport(sport_id:int):
    df = postgresql_to_dataframe(
    """
    SELECT name_sport 
    FROM supra.dict_sport ds 
    where id_sport = %s
    ;
    """%(sport_id),['name_sport'])
    name_sport = df.loc[0, 'name_sport']
    return name_sport

def school_name_school(school_id:int):
    df = postgresql_to_dataframe(
    """
    SELECT name_altarnative 
    FROM supra.dict_firm
    where id_firm = %s
    ;
    """%(school_id),['name_altarnative'])
    name_s = df.loc[0, 'name_altarnative']
    return name_s


def sport_mean_school(sport_id:int):
    column_names = ['Учреждение', 'Общая численность', 'НП', 'ТЭ', 
    'СС', 'ВСМ', 'Гос работа']
    df = postgresql_to_dataframe(
        """
        SELECT
        df.name_altarnative,
        sum(gos.total_sport) as total_sport,
        sum(gos.np) AS np,
        sum(gos.te) AS te,
        sum(gos.cc) AS cc,
        sum(gos.vcm) AS vcm,
        sum(gos.gos_work) AS gos_work
        FROM supra.gos_order gos
        INNER JOIN supra.dict_firm df ON gos.id_firm = df.id_firm 
        WHERE gos.archiv_data = '0'
        AND gos.id_sport = %s
        AND created_at = (
        SELECT 
        created_at 
        FROM supra.gos_order
        WHERE archiv_data = '0'
        GROUP BY created_at ORDER BY created_at DESC LIMIT 1
        )
        GROUP BY name_altarnative ORDER BY total_sport DESC 
        ;"""%(sport_id), column_names)
    df = df.astype({"Общая численность": int})
    return df

def sport_mean_school_past(sport_id:int):
    column_names = ['Учреждение', 'Общая численность', 'НП', 'ТЭ', 
    'СС', 'ВСМ', 'Гос работа']
    df = postgresql_to_dataframe(
        """
        SELECT
        df.name_altarnative,
        sum(gos.total_sport) as total_sport,
        sum(gos.np) AS np,
        sum(gos.te) AS te,
        sum(gos.cc) AS cc,
        sum(gos.vcm) AS vcm,
        sum(gos.gos_work) AS gos_work
        FROM supra.gos_order gos
        INNER JOIN supra.dict_firm df ON gos.id_firm = df.id_firm 
        WHERE gos.archiv_data = '0'
        AND gos.id_sport = %s
        AND created_at = (
            SELECT created_at
            FROM (
                SELECT created_at
                FROM supra.gos_order
                WHERE archiv_data = '0'
                GROUP BY created_at
                ORDER BY created_at DESC
                LIMIT 12
            ) AS subquery
            ORDER BY created_at ASC
            LIMIT 1
        )
        GROUP BY name_altarnative ORDER BY total_sport DESC 
        ;"""%(sport_id), column_names)
    df = df.astype({"Общая численность": int})
    return df


def sport_mean_fed(sport_id:int):
    column_names = ['name_fed', 'leader_job', 'leader_name', 'leader_contact', 'fed_date_rd', 
    'fed_date_finesh', 'fed_date_text', 'fed_rd', 'fed_website', 'fed_email', 'fed_contact', 'id_ogrn']
    df = postgresql_to_dataframe(
        """
        SELECT 
        name_fed, 
        leader_job, 
        leader_name,
        leader_contact, 
        fed_date_rd, 
        fed_date_finesh,
        fed_date_text,
        fed_rd,
        fed_website, 
        fed_email, 
        fed_contact,
        id_ogrn
        FROM supra.fed_order
        WHERE id_sport = %s
        AND archiv_data = '0'
        ;
        """%(sport_id), column_names)
    return df




def school_mean_sport(school_id:int):
    column_names = ['Вид спорта', 'Общая численность', 'НП', 'ТЭ', 
    'СС', 'ВСМ', 'Гос работа']
    df = postgresql_to_dataframe(
        """
        SELECT
        ds.name_sport as name_sport,
        sum(gos.total_sport) as total_sport,
        sum(gos.np) AS np,
        sum(gos.te) AS te,
        sum(gos.cc) AS cc,
        sum(gos.vcm) AS vcm,
        sum(gos.gos_work) AS gos_work
        FROM supra.gos_order gos
        INNER JOIN supra.dict_sport ds on gos.id_sport = ds.id_sport 
        WHERE gos.archiv_data = '0'
        AND created_at = (
        SELECT 
        created_at 
        FROM supra.gos_order
        WHERE archiv_data = '0'
        GROUP BY created_at ORDER BY created_at DESC LIMIT 1
        )
        AND gos.id_firm = %s
        GROUP BY name_sport ORDER BY name_sport 
        ;"""%(school_id), column_names)
    df = df.astype({"Общая численность": int})
    return df


def school_mean_sport_past(school_id:int):
    column_names = ['Вид спорта', 'Общая численность', 'НП', 'ТЭ', 
    'СС', 'ВСМ', 'Гос работа']
    df = postgresql_to_dataframe(
        """
        SELECT
            ds.name_sport AS name_sport,
            SUM(gos.total_sport) AS total_sport,
            SUM(gos.np) AS np,
            SUM(gos.te) AS te,
            SUM(gos.cc) AS cc,
            SUM(gos.vcm) AS vcm,
            SUM(gos.gos_work) AS gos_work
        FROM supra.gos_order gos
        INNER JOIN supra.dict_sport ds ON gos.id_sport = ds.id_sport
        WHERE gos.archiv_data = '0'
        AND created_at = (
            SELECT created_at
            FROM (
                SELECT created_at
                FROM supra.gos_order
                WHERE archiv_data = '0'
                GROUP BY created_at
                ORDER BY created_at DESC
                LIMIT 8
            ) AS subquery
            ORDER BY created_at ASC
            LIMIT 1
        )
        AND gos.id_firm = %s
        GROUP BY name_sport
        ORDER BY name_sport
        ;"""%(school_id), column_names)
    df = df.astype({"Общая численность": int})
    return df

def school_mean_curator(school_id:int):
    column_names = ['name_curator', 'contakt_tel', 'contakt_email']
    df = postgresql_to_dataframe(
        """
        SELECT name_curator,contakt_tel,contakt_email
        FROM supra.dict_curator_firm dcf 
        where id_firm = %s
        ;"""%(school_id), column_names)
    return df


def school_mean_firm(school_id:int):
    column_names = ['name_altarnative' , 'name_full', 'ogrn', 
    'contakt_email', 'contakt_tel', 'contakt_url', 'firm_url']
    df = postgresql_to_dataframe(
        """
        SELECT
        df.name_altarnative,
        df.name_full,
        df.ogrn,
        df.contakt_email,
        df.contakt_tel,
        df.contakt_url,
        df.firm_url
        FROM supra.dict_firm df
        WHERE df.id_firm = %s
        ;"""%(school_id), column_names)
    return df

def school_led_firm(school_id:id):
    column_names = ['name_job' , 'name_led', 'led_cotakt', 'led_mail']
    df = postgresql_to_dataframe(
        """
        SELECT 
        name_job,
        name_leader,
        contakt_tel,
        contakt_email 
        FROM supra.dict_leader_firm
        WHERE archiv_leader ='0'
        AND id_firm = %s
        ;"""%(school_id), column_names)
    return df

def sport_mean_fk5_r5(sport_id:int):
    column_names = ['total_sport', 'total_other', 'total_1r', 'total_kms', 
    'total_ms', 'total_msmk', 'total_zms', 'total_grm']
    df = postgresql_to_dataframe(
        """
        SELECT 
        sum(total_sport) as total_sport,
        sum(rank_r_other) as total_other,
        sum(rank_r_1r) as total_1r,
        sum(rank_r_kms) as total_kms,
        sum(rank_z_ms) as total_ms,
        sum(rank_z_msmk) as total_msmk,
        sum(rank_z_zms) as total_zms,
        sum(rank_z_grm) as total_grm
        FROM supra.fk_order_r5 r5
        where id_sport = %s
        and archiv_data = '0'
        and reporting_year = (
        SELECT reporting_year 
        FROM supra.fk_order_r5
        where archiv_data = '0'
        group by reporting_year order by reporting_year DESC LIMIT 1
        )
        ;"""%(sport_id), column_names)

    return df


def sport_mean_fk5_r9(sport_id:int):
    column_names = ['trainers', 'ztr']
    df = postgresql_to_dataframe(
        """
        SELECT 
        sum(total_trainers) as trainers,
        sum(rank_ztr) as ztr
        FROM supra.fk_order_r9 
        where id_sport = %s
        and archiv_data = '0'
        and reporting_year =
        (
        select reporting_year 
        FROM supra.fk_order_r9
        where archiv_data  = '0'
        group by reporting_year order by reporting_year DESC LIMIT 1
        )
        ;"""%(sport_id), column_names)
    
    return df
