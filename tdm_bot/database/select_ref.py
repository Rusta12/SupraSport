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


