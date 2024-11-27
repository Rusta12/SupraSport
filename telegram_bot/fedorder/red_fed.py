import pandas as pd
#Mod
from fedorder.fed_reference import token_sport



#Вставка id вида спорта
def load_fed_name(name_file):
    df = pd.read_excel(name_file)
    #Чистка первая
    df = df.replace(r"\n", " ",  regex=True)
    df = df.fillna('нет данных')
    #Исправление пробелов и кавычек
    df = replase_probel(df)
    df = replace_quotes(df)
    df[df.columns[7]] = pd.to_datetime(df[df.columns[7]]).dt.strftime('%Y-%m-%d')
    df = df.rename(columns={df.columns[2]: 'name_sport'})
    df['name_sport'] = df['name_sport'].str.lower()
    #Загрузка данных из БД
    df_bd = token_sport()
    df_bd['name_sport'] = df_bd['name_sport'].str.lower()
    #Мердж данных
    df = df.merge(df_bd, on='name_sport', how='left')
    #df = df.drop_duplicates(subset=['name_sport'])
    #df = mask(df, df_bd)
    #df = df.dropna(subset=['id'])
    #Подготовка перед отправкой в БД
    #df['id'] = df['id'].astype(int)
    df = df[[df.columns[4], 'id', df.columns[3], df.columns[5],
            df.columns[6], df.columns[7], df.columns[8], df.columns[9],
            df.columns[10], df.columns[11], df.columns[12], df.columns[13],
            df.columns[14], df.columns[15], df.columns[16]]]
    df[df.columns[11]] = df[df.columns[11]].astype(str)
    return df


def mask(df, df_bd):
    mask = df[['id']].isna().any(axis=1)
    df_n = df[mask]
    for x in range(df_bd.shape[0]):
        df_sersh = df_n[(df_n['name_sport'].str.startswith(str(df_bd.loc[x, 'name_sport'])))]
        if df_sersh.shape[0] != 0:
            df_n.loc[df_sersh.index[0], 'id'] = df_bd.loc[x, 'id']
        else:
            pass
    df = pd.concat([df, df_n])
    return df

def replase_probel(df):
    probel = ' '
    for i in range(70):
        probel = probel + ' '
        df = df.replace(probel, " ",  regex=True)
    probel = ' '
    for i in range(10):
        probel = probel + ' '
        df = df.replace(probel, " ",  regex=True)
    df[df.columns[8]] = df[df.columns[8]].str.strip()
    df[df.columns[3]] = df[df.columns[3]].str.strip()
    df[df.columns[5]] = df[df.columns[5]].str.strip()
    df[df.columns[6]] = df[df.columns[6]].str.strip()
    df[df.columns[11]] = df[df.columns[11]].str.strip()
    #df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.apply(lambda x: x.map(lambda y: y.strip() if isinstance(y, str) else y))
    return df

def replace_quotes(df):
    quotes_start = ' »'
    quotes_finesh = '"'
    df = df.replace(quotes_finesh, "»",  regex=True)
    df = df.replace(quotes_start, " «",  regex=True)
    return df



