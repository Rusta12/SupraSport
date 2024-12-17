import pandas as pd
#Mod
import gosorder.update_gosorder.reference as rf
from gosorder.update_gosorder.colum_drop import drop_general
from gosorder.update_gosorder.colum_gos_order import col_gos




def read_excel(name_file:str, sheet_firm:str):
    xls = pd.ExcelFile(f'{name_file}')
    df = pd.read_excel(xls, sheet_name=sheet_firm)
    return df

#Вставка организации
def name_firm(df, id_firm:int):
    df.insert(0, 'Учреждение', id_firm)
    return df

#Вставка вида спорта
def name_sport(df, df_sport):
    df['Вид спорта'] = df['Вид спорта'].replace(r"\n", " ",  regex=True)
    df['Вид спорта'] = df['Вид спорта'].str.lower()
    for x in range(df.shape[0]):
        for y in range(df_sport.shape[0]):
            if  df.loc[x, 'Вид спорта'] == df_sport.loc[y, 'Вид спорта']:
                df.loc[x, 'Вид спорта'] = df_sport.loc[y, 'id_sport']

    return df

#Имя таблицы
def name_df(df, name_file: str):
    df['Имя файла'] = name_file
    df['Имя файла'] = df['Имя файла'].replace(r"Свод ", "",  regex=True)
    df['Имя файла'] = df['Имя файла'].replace(r".xlsx", "",  regex=True)
    df['Имя файла'] = df['Имя файла'].replace(r"./gosorder/update_gosorder/Temp/", "",  regex=True)
    return df

def astype_df(df):
    df['СС1'] = df['СС1'].replace(r" ", 0,  regex=True)

    columns_to_convert = ['Учреждение', 'Вид спорта', 'Общая численность',
                         'НП1', 'НП2', 'НП3', 'НП4', 'НП', 
                         'ТЭ1', 'ТЭ2','ТЭ3', 'ТЭ4', 'ТЭ5', 'ТЭ', 
                         'СС1', 'СС2', 'СС3', 'СС', 
                         'ВСМ', 'Гос работа']
    df[columns_to_convert] = df[columns_to_convert].astype(int)


    df['НП пк'] = df['НП пк'].map(lambda x: round(x, 1))
    df['ТЭ пк'] = df['ТЭ пк'].map(lambda x: round(x, 1))
    df['СС пк'] = df['СС пк'].map(lambda x: round(x, 1))
    df['ВСМ пк'] = df['ВСМ пк'].map(lambda x: round(x, 1))
    return df



#Полная обработака
def general_concat(name_file):
    sheets_firm= rf.firm()
    df_sport = rf.token_sport()
    df_data = pd.DataFrame(columns=col_gos)
    for x in range(sheets_firm.shape[0]):
        sheet_firm = sheets_firm.loc[x, 'name_short']
        print(sheet_firm)
        id_firm = sheets_firm.loc[x, 'id_firm']
        df =  read_excel(name_file, sheet_firm)
        df = drop_general(df)
        df = name_firm(df, id_firm)
        df_data = pd.concat([df_data, df])
    df_data = df_data.reset_index(drop=True)
    df_data = name_sport(df_data, df_sport)
    df_data = name_df(df_data, name_file)
    df_data = astype_df(df_data)
    return df_data


#Тестовая обработка
def test_concat(name_file, name_school:str):
    sheets_firm= rf.firm()
    sheets_firm = sheets_firm[(sheets_firm['name_short'] == name_school)].reset_index(drop=True)
    sheet_firm = sheets_firm.loc[0, 'name_short']
    id_firm = sheets_firm.loc[0, 'id_firm']
    df_sport = rf.token_sport()
    df_data = pd.DataFrame(columns=col_gos)
    df =  read_excel(name_file, sheet_firm)
    print('1')
    df = drop_general(df)
    print('2')
    df = name_firm(df, id_firm)
    print('3')
    df_data = pd.concat([df_data, df])
    df_data = df_data.reset_index(drop=True)
    df_data = name_sport(df_data, df_sport)
    df_data = name_df(df_data, name_file)
    df_data = astype_df(df_data)
    return df_data
