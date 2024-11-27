import numpy as np
import pandas as pd


column_general_view = ['№ п/п',
 'Наименование вида спорта',
 'Номер-код вида спорта',
 'код вида спорта 3',
 'код вида спорта 4',
 'код вида спорта 5',
 'код вида спорта 6',
 'код вида спорта 7',
 'код вида спорта 8',
 'Наименование спортивной дисциплины',
 'Номер-код спортивной дисциплины',
 'код дисциплины 1',
 'код дисциплины 2',
 'код дисциплины 3',
 'код дисциплины 4',
 'код дисциплины 5',
 'код дисциплины 6']

column_admitted_view = ['№ п/п',
 'Наименование вида спорта',
 'Номер-код вида спорта',
 'код вида спорта 3',
 'код вида спорта 4',
 'код вида спорта 5',
 'код вида спорта 6',
 'код вида спорта 7',
 'код вида спорта 8',
 'Наименование спортивной дисциплины',
 'Номер-код спортивной дисциплины',
]


def general_view_sport(file_path):
    sheet_name = 'Общероссийские'
    xlsm = pd.ExcelFile(file_path)
    df = pd.read_excel(xlsm, sheet_name)
    #Функция для обработки общероссийской
    df = df.drop(df.index[:6])
    df = df.reset_index(drop=True)
    df.columns = column_general_view
    df_sport = df[['Номер-код вида спорта', 
                   'Наименование вида спорта',]]
    df_sport['Раздел'] = sheet_name
    #Удаление пробелов
    df_sport['Наименование вида спорта'] = df_sport['Наименование вида спорта'].str.rstrip()
    df_sport = df_sport.dropna()
    df_sport = df_sport.reset_index(drop=True)
    
    return df_sport

def admitted_view_sport(file_path):
    sheet_name = 'Признанные'#Национальные Прикладные
    xlsm = pd.ExcelFile(file_path)
    df = pd.read_excel(xlsm, sheet_name)
    df = df.drop(df.index[:4])
    df = df.reset_index(drop=True)
    df.columns = column_admitted_view
    df = df[['Номер-код вида спорта', 
                   'Наименование вида спорта',]]
    df['Раздел'] = sheet_name
    df['Наименование вида спорта'] = df['Наименование вида спорта'].str.rstrip()
    df = df.dropna()
    df = df.reset_index(drop=True)

    return df

def national_view_sport(file_path):
    sheet_name = 'Национальные' #Прикладные
    xlsm = pd.ExcelFile(file_path)
    df = pd.read_excel(xlsm, sheet_name)
    df = df.drop(df.index[:7])
    df = df.reset_index(drop=True)
    df.columns = column_general_view
    df = df[['Номер-код вида спорта', 
                   'Наименование вида спорта',]]
    df['Раздел'] = sheet_name
    df['Наименование вида спорта'] = df['Наименование вида спорта'].str.rstrip()
    df = df.dropna()
    df = df.reset_index(drop=True)

    return df


def applied_view_sport(file_path):
    sheet_name = 'Прикладные'
    xlsm = pd.ExcelFile(file_path)
    df = pd.read_excel(xlsm, sheet_name)
    df = df.drop(df.index[:6])
    df = df.reset_index(drop=True)
    df.columns = column_general_view
    df = df[['Номер-код вида спорта', 
                   'Наименование вида спорта',]]
    df['Раздел'] = sheet_name
    df['Наименование вида спорта'] = df['Наименование вида спорта'].str.rstrip()
    df = df.dropna()
    df = df.reset_index(drop=True)

    return df


def concat_view_sport(file_path):
    df_general = general_view_sport(file_path)
    df_admitted = admitted_view_sport(file_path)
    df_national = national_view_sport(file_path)
    df_applied = applied_view_sport(file_path)
    df = pd.concat([df_general, df_admitted, df_national, df_applied], ignore_index=True)
    return df

