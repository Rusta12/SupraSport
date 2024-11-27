import pandas as pd

#Mod
from gosorder.update_gosorder.colum_gos_order import col_drop

def colum_name(df):
    #Убираем столбик с ФКиС
    if df.iloc[1,2] == 'ФКиС':
        df = df.drop(df.columns[[2]], axis=1)
    else:
        pass
    #Назначаем заголовки столбцов
    if df.shape[1] == 22:
        df.insert(5, 'НП4', 0)
    df = df.set_axis(col_drop, axis='columns')
    #Убираем лишние строки сверху
    if df.iloc[2,0] == 1:
        df.drop(df.index[[0,1,2]], inplace=True)
    elif df.iloc[3,0] == 1:
        df.drop(df.index[[0,1,2,3]], inplace=True)
    elif df.iloc[4,0] == 1:
        df.drop(df.index[[0,1,2,3,4]], inplace=True)
    elif df.iloc[5,0] == 1:
        df.drop(df.index[[0,1,2,3,4,5]], inplace=True)
        
    return df

#Удаляем строчку с итогами
def drop_total(df):
    df_index_upper = df.loc[df['Вид спорта'].str.contains(r"\bИТОГО\b", na=False)]
    df_index_title = df.loc[df['Вид спорта'].str.contains(r"\bИтого\b", na=False)]
    if df_index_upper.shape[0] != 0:
        for x in df_index_upper.index:
            df.drop([x], inplace=True)
    if df_index_title.shape[0] != 0:
        for x in df_index_title.index:
            df.drop([x], inplace=True)
    return df

#Удаляем остальное
def drop_over(df):
    df_fix = df.loc[df['Вид спорта'].str.contains(r"\bв т.ч\b", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Спорт глухих:", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Спорт слепых:", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Спорт ПОДА:", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Спорт лиц с поражением ОДА:", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Спорт лиц  с интеллектуальными нарушениями:", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    return df

#Удаляем нули
def drop_zero(df):
    df = df.fillna(0)
    df_zero = df[df['Общая численность'] == 0]
    if df_zero.shape[0] != 0:
        for x in df_zero.index:
            df.drop([x], inplace=True)
    return df


#Объединяем
def drop_general(df):
    df = colum_name(df)
    df = drop_total(df)
    df = drop_over(df)
    df = drop_zero(df)

    return df


