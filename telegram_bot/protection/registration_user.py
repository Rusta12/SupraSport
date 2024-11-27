from telebot import types
from config import bot
#Mod
from protection.protection_insert import chek_user_count, add_user_bd, chek_user_profile




#Первый заход пользователя и его регистрация с ролью 0
def add_user(message):
	user = chek_user_count(message.chat.id)
	if user == 0:
		add_user_bd(message.chat.id, message.from_user.first_name, message.from_user.username)
		add_access(message)
	else:
		pass 


def add_access(message):
    """
    Функция отправки запрос по доступу
    """
    bot.send_message(
        message.chat.id,
        text='У вас отсутствует необходимый уровень доступа.'
        		'\nДля получения доступа к разделам Аналитик СУ обратитесь к @RusBul'
        		'\nВ сообщении укажите:'
        		'\n<b>Имя и Фамилию:</b>'
        		'\n<b>Организация:</b>'
        		'\n<b>Адрес электронной почты:</b>'
        		'\n<b>Номер телефона:</b>'
        		f'\n<b>ID в телеграмм:</b> <i>ваш номер - {message.chat.id}</i>',
        		parse_mode="HTML")
    return


def profile_user_print(message):
    """
    Функция отправки запрос по доступу
    """
    df = chek_user_profile(message.chat.id)
    role_access = df.loc[0, 'id_role_access']
    if role_access == 0:
        role = 'ограниченый'
    elif role_access == 1:
        role = 'минимальный'
    elif role_access == 2:
        role = 'средний'
    elif role_access == 3:
        role = 'макисимальный'
    username = df.loc[0, 'username']
    bot.send_message(
        message.chat.id,
        text=f'<b>Ваш уровень доступа -</b> <i>{role}!</i>'
                f'\n<b>Имя:</b> - <i>{username}</i>'
                f'\n<b>ID в телеграмм:</b> <i>номер - {message.chat.id}</i>'
                f'\n<b>Уровень пользователя -</b> <i>новичок.</i>'
                '\n<b>Дней до отпуска</b> - <i>пока в разработке.</i>'
                '\nЗакрепи меня в свой чат лист, что бы мы не потерялись 👍',
                parse_mode="HTML")
    return

#профиль пользователя
def profile_user(message):
    user = chek_user_count(message.chat.id)
    if user == 0:
        add_user_bd(message.chat.id, message.from_user.first_name, message.from_user.username)
    else:
        pass
    return profile_user_print(message)
