"""SQL-запросы для списков из главного меню бота (xlsx-выгрузки).

Таблицы живут в legacy-схеме `supra`, поэтому здесь запросы квалифицированы
явно — в отличие от схемы tdm_bot, где работает search_path.
"""

import logging

from database.conn_db import postgresql_to_dataframe, postgresql_to_dataframe_params

logger = logging.getLogger(__name__)

_ORG_COLUMNS = [
    'Организация',
    'Тип',
    'Руководитель',
    'E-mail',
    'Сайт',
    'Полное наименование',
]

_ORG_SQL = """
    SELECT
        df.name_altarnative_ias,
        df.type_firm,
        ld.name_leader,
        df.contakt_email,
        df.contakt_url,
        df.name_full
    FROM supra.dict_firm df
    LEFT JOIN supra.dict_leader_firm ld
           ON df.id_firm = ld.id_firm
          AND ld.archiv_leader = false
    WHERE df.archiv_sport = false
      AND df.sub_org = %s
    ORDER BY df.name_altarnative_ias
    ;
"""


def select_organizations_moskomport():
    """Учреждения в системе Москомспорта (sub_org = true).

    SQL предоставлен пользователем; колонки отчёта переопределены русскими
    алиасами, чтобы в .xlsx были понятные заголовки.
    """
    return postgresql_to_dataframe_params(_ORG_SQL, _ORG_COLUMNS, (True,))


def select_organizations_other():
    """Другие учреждения (с лицензией): sub_org = false."""
    return postgresql_to_dataframe_params(_ORG_SQL, _ORG_COLUMNS, (False,))


def select_federations():
    """Актуальные аккредитованные федерации.

    В fed_order на одну федерацию (id_ogrn) десятки строк — записи по годам.
    Берём ТУ запись, что добавлена последней (max(created_at)), и только те,
    чья аккредитация ещё действует (fed_date_finesh >= текущая дата).
    На данных стенда выходит 152 федерации из 179 возможных.
    """
    column_names = [
        'Федерация',
        'Вид спорта',
        'Должность руководителя',
        'Руководитель',
        'Контакты руководителя',
        'Адрес',
        'Телефон',
        'E-mail',
        'Сайт',
        'Распоряжение',
        'Дата распоряжения',
        'Аккредитация до',
    ]
    return postgresql_to_dataframe(
        """
        SELECT
            f.name_fed,
            s.name_sport,
            f.leader_job,
            f.leader_name,
            f.leader_contact,
            f.fed_addres,
            f.fed_contact,
            f.fed_email,
            f.fed_website,
            f.fed_rd,
            f.fed_date_rd,
            f.fed_date_finesh
        FROM supra.fed_order f
        LEFT JOIN supra.dict_sport s ON s.id_sport = f.id_sport
        WHERE f.archiv_data = false
          AND f.id_ogrn IN (
              SELECT id_ogrn FROM supra.fed_order
              WHERE archiv_data = false
              GROUP BY id_ogrn
          )
          AND f.created_at = (
              SELECT max(created_at) FROM supra.fed_order
              WHERE id_ogrn = f.id_ogrn AND archiv_data = false
          )
          -- «актуальные»: аккредитация действует. Убрать условие, чтобы
          -- включить все федерации по дате добавления (179 вместо 152)
          AND f.fed_date_finesh >= current_date
        ORDER BY s.name_sport, f.name_fed
        ;
        """,
        column_names)