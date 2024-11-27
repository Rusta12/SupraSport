import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager



def get_school_kpi(message, df):
    # Укажите путь к файлу шрифта
    font_path = 'ofont.ru_Times New Roman.ttf'  # Убедитесь, что путь правильный
    font_prop = font_manager.FontProperties(fname=font_path)

    # Подготовка данных для визуализации
    df['change'] = df['Общая численность_today'] - df['Общая численность_past']
    df['color'] = ['green' if change > 0 else 'red' if change < 0 else 'grey' for change in df['change']]

    # Сортировка по общей численности
    df.sort_values('Общая численность_today', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Определение размера фигуры в зависимости от количества видов спорта
    num_sports = len(df)
    fig_height = max(num_sports * 0.5, 2)  # Минимальная высота фигуры 8 дюймов
    # Ширина фигуры фиксированная, можно настроить при необходимости
    if df.iloc[0]['Общая численность_past'] > 100:
        if num_sports <= 2:
            fig_width = 3
        else:
            fig_width = 12
    else:
        fig_width = 8  #другая ширина, если условие не выполнено

    # Построение графика
    plt.figure(figsize=(fig_width, fig_height), dpi=80)

    # График изменения с цветовой шкалой
    for i, (total, change, color) in enumerate(zip(df['Общая численность_today'], df['change'], df['color'])):
        plt.hlines(y=i, xmin=0, xmax=total, color='grey', alpha=0.3, linewidth=4)  # Основная шкала
        plt.hlines(y=i, xmin=total - change, xmax=total, color=color, alpha=0.7, linewidth=4)  # Шкала изменений
        # Добавление текста с цветовым кодированием
        if num_sports == 1:
            # Условное положение для одного вида спорта
            plt.text(total + 10, i, f'{total}',  # Положение текста для общей численности немного выше
                    horizontalalignment='left', 
                    verticalalignment='center', 
                    color='black', 
                    fontsize=12, weight='bold')
            
            plt.text(total + 10, i - 0.01, f'{change:+}',  # Положение текста для изменений немного ниже
                    horizontalalignment='left', 
                    verticalalignment='center', 
                    color=color, 
                    fontsize=12, weight='bold')
        else:
            plt.text(total + 10, i + 0.2, f'{total}',  # Положение текста для общей численности немного выше
                    horizontalalignment='left', 
                    verticalalignment='center', 
                    color='black', 
                    fontsize=12, weight='bold')
            
            plt.text(total + 10, i - 0.2, f'{change:+}',  # Положение текста для изменений немного ниже
                    horizontalalignment='left', 
                    verticalalignment='center', 
                    color=color, 
                    fontsize=12, weight='bold')

    # Настройки
    plt.yticks(df.index, df['Вид спорта'], fontsize=14)
    plt.title('Изменение общей численности за 8 периодов государственного задания.', fontdict={'size':20, 'fontproperties': font_prop}, pad=25)

    # Удаление линий и границ
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    plt.grid(False)  # Удаление сетки
    plt.xticks([])   # Удаление делений по оси X
    # Увеличиваем отступы, чтобы избежать наложения заголовка
    plt.subplots_adjust(top=0.85)
    #plt.show()
    image_name = f'./gosorder/reporter_gosorder/Temp/schoo_kpi_{message.chat.id}.png'
    plt.savefig(image_name , transparent=True, bbox_inches='tight', dpi = 80)
    return image_name
    