import pandas as pd
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#Mod




def kpi_chronology(message, df):
	#plt.rcParams["font.family"] = "Times New Roman"
	plt.rcParams.update({'font.size': 14})
	fig, ax = plt.subplots(figsize=(12,12))

	bottom = np.zeros(df.shape[0])

	df['Гос задание'] = df['Гос задание'].replace('ГЗ 1 ', '1 ', regex=True)
	df['Гос задание'] = df['Гос задание'].replace('2022', '22г.', regex=True)
	df['Гос задание'] = df['Гос задание'].replace('2023', '23г.', regex=True)
	df['Гос задание'] = df['Гос задание'].replace('2024', '24г.', regex=True)

	df_arr = df[['НП', 'ТЭ', 'СС', 'ВСМ', 'Гос работа']].to_numpy().T
	df_colum = ['НП', 'ТЭ', 'СС', 'ВСМ', 'Гос работа']

	for x in df_arr:
		p = ax.bar(df['Гос задание'], x, bottom=bottom)
		bottom += x
		ax.bar_label(p, 
						labels=[f'{val:,.0f}'.replace(',', ' ') for val in x], 
						label_type='center', fontsize=11
					)
	for i, val in enumerate(df['Общий'].values):
		plt.text(i, val, str('{:,}'.format(val).replace(',', ' ')), 
								horizontalalignment='center', 
								verticalalignment='bottom', 
								fontdict={'fontweight':650, 'size':14})
	    
	ax.set(title='Хронология', ylabel='Объемы занимающихся', xlabel='Гос. задание по месяцам')
	ax.legend(df_colum, shadow=True, loc="center left", bbox_to_anchor=(1.0, -0.8, 0.5, 2.8))
	plt.xticks(df['Гос задание'], rotation=45, horizontalalignment='center')
	image_name = f'./gosorder/reporter_gosorder/Temp/chronology_{message.chat.id}.png'
	plt.savefig(image_name , transparent=True, bbox_inches='tight', dpi = 80)
	return image_name


