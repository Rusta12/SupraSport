from database.conn_db import postgresql_to_dataframe

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


def school_mean_curator(school_id:int):
    column_names = ['name_curator', 'contakt_tel', 'contakt_email']
    df = postgresql_to_dataframe(
        """
        SELECT name_curator,contakt_tel,contakt_email
        FROM supra.dict_curator_firm dcf 
        where id_firm = %s
        AND archiv_curator = '0'
        ;"""%(school_id), column_names)
    return df


def school_rank_statistics(school_id:int):
    column_names = ['total_sport', 'total_other', 'total_1r', 'total_kms', 
    'total_ms', 'total_msmk', 'total_zms', 'total_grm']
    df = postgresql_to_dataframe(
        """
        SELECT 
            COUNT(*) AS total_sport,
            COUNT(CASE WHEN id_razryad IN (24,25,26,27,28) THEN 1 END) AS total_other,
            COUNT(CASE WHEN id_razryad IN (115) THEN 1 END) AS total_1r,
            COUNT(CASE WHEN id_razryad IN (30) THEN 1 END) AS total_kms,
            COUNT(CASE WHEN id_razryad IN (31) THEN 1 END) AS total_ms,
            COUNT(CASE WHEN id_razryad IN (32) THEN 1 END) AS total_msmk,
            COUNT(CASE WHEN id_razryad IN (129) THEN 1 END) AS total_zms,
            COUNT(CASE WHEN id_razryad IN (135) THEN 1 END) AS total_grm
        FROM supra.sports_rank_statistics srs
        WHERE id_firm = %s
        AND created_at = (
        SELECT created_at  FROM supra.sports_rank_statistics
        WHERE archiv_qualification = '0'
        GROUP BY created_at  ORDER BY created_at DESC LIMIT 1
        )
        ;"""%(school_id), column_names)

    return df

def school_stat_trainer(school_id:int):
    column_names = column_names = ['trainers', 'ztr', 'age_to_35', 'age_36_to_64', 'age_64_to_old']
    df = postgresql_to_dataframe(
        """
        SELECT 
        sum(total_trainers) as trainers,
        sum(rank_ztr) as ztr,
        sum(age_to_35) as age_to_35,
        sum(age_36_to_64) as age_36_to_64,
        sum(age_64_to_old) as age_64_to_old
        FROM supra.stat_report_trainer
        where id_firm = %s
        and archiv_data = '0'
        and reporting_year =
        (
        select reporting_year 
        FROM supra.stat_report_trainer
        where archiv_data  = '0'
        group by reporting_year order by reporting_year DESC LIMIT 1
        )
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

def school_led_firm(school_id:int):
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
