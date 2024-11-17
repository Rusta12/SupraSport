import telebot
import os

# Получаем токен бота из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
