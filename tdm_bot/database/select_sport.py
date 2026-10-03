from database.conn_db import postgresql_to_dataframe


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
        ORDER BY created_at DESC
        LIMIT 1;
        """%(sport_id), column_names)
    return df

def sport_rank_statistics(sport_id:int):
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
        WHERE id_sport = %s
        AND created_at = (
        SELECT created_at  FROM supra.sports_rank_statistics
        WHERE archiv_qualification = '0'
        GROUP BY created_at  ORDER BY created_at DESC LIMIT 1
        );
        """%(sport_id), column_names)

    return df

def sport_stat_trainer(sport_id:int):
    column_names = ['trainers', 'ztr', 'age_to_35', 'age_36_to_64', 'age_64_to_old']
    df = postgresql_to_dataframe(
        """
        SELECT 
        sum(total_trainers) as trainers,
        sum(rank_ztr) as ztr,
        sum(age_to_35) as age_to_35,
        sum(age_36_to_64) as age_36_to_64,
        sum(age_64_to_old) as age_64_to_old
        FROM supra.stat_report_trainer
        where id_sport = %s
        and archiv_data = '0'
        and reporting_year =
        (
        select reporting_year 
        FROM supra.stat_report_trainer
        where archiv_data  = '0'
        group by reporting_year order by reporting_year DESC LIMIT 1
        )
        ;"""%(sport_id), column_names)
    
    return df