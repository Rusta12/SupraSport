from config import bot
from telebot import types
import os
#Mod
from protection.check_prot import validation_user
from fedorder.fed_reference import fed_to_id_tuple, arhiv_id_fed, fed_add_to_bd
from fedorder.red_fed import load_fed_name
from database.attributs import upd_loger_finishhim


def fed_upload_file(message):
    if validation_user(message, 2) == True:
        pass
    else:
        return
    bot.send_message(
		message.chat.id,
		text='📌Перед отправкой файла убедитесь, пожалуйста, в следующем'
	          '\n1. Файл должен быть в виде «excel».'
	          '\n2. Предыдущие данные будут перемещены в архив.'
	          )
    #тут инструкция и сообщение о содержании файла
    bot.send_message(message.chat.id, text="Отправьте мне файл.")
    @bot.message_handler(content_types=['document'])
    def send_file_fed(message):
        msg = bot.send_message(message.chat.id, "Файл в обработке, ожидайте пожалуйста!")
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            path_file = f'./fedorder/Temp/{message.document.file_name}'
            with open(path_file, 'wb') as new_file:
                new_file.write(downloaded_file)
            with open('./bot_documents/gif/batut.mp4', 'rb') as gif:
                msv = bot.send_video(message.chat.id, gif, None)
            id_fed = fed_to_id_tuple()
            df = load_fed_name(path_file)
            fed_add_to_bd(df)
            arhiv_id_fed(id_fed)
            bot.send_message(message.chat.id, f"Файл успешно обработан.")
            bot.delete_message(message.chat.id, msg.message_id)
            bot.delete_message(message.chat.id, msv.message_id)
            upd_loger_finishhim(message, 'fed_load_data', 'reload_data')
        except Exception as e:
            bot.send_message(message.chat.id, f"При обработке файла возникла ошибка {e}")
            os.remove(path_file)
            bot.delete_message(message.chat.id, msg.message_id)
            bot.delete_message(message.chat.id, msv.message_id)



