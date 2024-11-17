from telebot import types
#Модули
from config import bot


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.delete_message(message.chat.id, message.message_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(
        message.chat.id, 
        text=f"Приветствую Вас, @{message.from_user.first_name}!\n"
        "Я Чатбот ТЕСТ.\n"
        "\n=================================================\n"
        "В настоящее время нахожусь в разработке, по вопросам обращайтесь к моему создателю @RusBul"
        "\n\nЗакрепи меня в свой чат лист, что бы мы не потерялись 👍"
        )
    return general_menu(message)



@bot.message_handler(content_types=['text'])
def mean_message(message):
    text = "Ну написал и написал, а дальше что ?"
    bot.send_message(message.chat.id, text)

    
if __name__ == "__main__":
    bot.infinity_polling()
