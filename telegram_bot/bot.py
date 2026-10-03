import telebot
from telebot import types
from config import bot
#Mod
from algoritm_message import algoritm_ai
from protection.registration_user import add_user, profile_user


@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    photo = open('./bot_documents/logo.jpg', 'rb')
    f = open('./bot_documents/Text_bot_information.txt', 'rt')
    content = f.read()
    bot.send_photo(message.chat.id, photo)
    bot.send_message(
        message.chat.id, 
        text=f"Приветствую Вас, @{message.from_user.first_name}!\n"
        "Я — продвинутый спортивный бот Спортивного управления Москомспорта и разбирающийся в статистике.\n"
        "\n=================================================\n"
        "В настоящее время нахожусь в разработке, по вопросам обращайтесь к моему создателю @RusBul"
        "\nЗакрепи меня в свой чат лист, что бы мы не потерялись 👍"
        )
    bot.send_message(
        message.chat.id, 
        content, 
        disable_web_page_preview=True, 
        parse_mode='Markdown', 
        reply_markup=markup
        )
    menu_gos_temp(message)
    add_user(message)
  
@bot.message_handler(commands=['profile'])
def profile_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    profile_user(message)




@bot.message_handler(content_types=['text'])
def mean_message(message):
    return algoritm_ai(message)



#Временное Меню(УДАЛИТЬ когда будет модель ИИ !)
def menu_gos_temp(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("ГОС задание")
    button2 = types.KeyboardButton("Федерации")
    markup.row(button1, button2)
    bot.send_message(
        message.chat.id, 
        text="Попробуй у меня что-нибудь спросить", 
        reply_markup=markup
        )

bot.infinity_polling()