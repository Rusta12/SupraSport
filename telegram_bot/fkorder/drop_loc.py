import pandas as pd
import warnings

warnings.filterwarnings('ignore')


#Удаляем нули
def drop_zero(df):
    df = df.fillna(0)
    df_zero = df[df['Разряды, звания Всего'] == 0]
    if df_zero.shape[0] != 0:
        for x in df_zero.index:
            df.drop([x], inplace=True)
    return df


#Удаляем остальное
def drop_over(df):
    df_fix = df.loc[df['Вид спорта'].str.contains(r"\bв том числе\b", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Ведомственная принадлежность\b", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Баскетбол (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Баскетбол 3х3", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Скелетон", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Маунтинбайк", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Трек", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Шоссе", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Водное поло (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Волейбол (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Пляжный волейбол (муж.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Пляжный волейбол (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Гандбол (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Гребля-индор", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Народная гребля", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Прибрежная гребля", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Керлинг (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Кёрлинг – смешанные пары", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Шорт-трек", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Бег на средние дистанции и бег с препятствиями", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Бег на длинные и сверхдлинные дистанции", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Многоборья", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Прыжки", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Метания", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Спортивная ходьба", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Открытая вода", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Прыжки в открытый водоем", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Двойной минитрамп", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Индивидуальные прыжки", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Синхронные прыжки", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Пневматический пистолет", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Малокалиберная винтовка", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Малокалиберный пистолет", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Движущаяся мишень", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Регби 7", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Регби - пляжное", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Регби на снегу", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Греко-римская борьба", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Грэпплинг", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Грэпплинг-ги", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Панкратион", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Скит", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Дубль-трап", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Спортинг", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"\bБлочный лук", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"\bАчери ", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Брейкинг", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Сабля", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Шпага", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Арт-фехтование", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Биг-эйр", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Могул", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Ски-кросс", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Хаф-пайп", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Слоуп-стайл", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Футбол (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Мини-футбол (футзал)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Пляжный футбол", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Футбол 6х6, 7х7, 8х8", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Интерактивный футбол", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Хоккей (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"Хоккей на траве (жен.)", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    df_fix = df.loc[df['Вид спорта'].str.contains(r"ИТОГО", na=False)]
    if df_fix.shape[0] != 0:
        for x in df_fix.index:
            df.drop([x], inplace=True)
    return df