import telebot
import settings


bot = telebot.TeleBot(settings.TOKEN)

openaiapi = settings.OPENAI

catalog_ya = settings.CATALOG_ID
ya_api = settings.Y_Api_Key
