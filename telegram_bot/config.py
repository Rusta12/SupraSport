import telebot
import settings
from telebot import apihelper
import socks
import time

"""
def setup_mtproto_proxy():
    print(f"🔄 Настройка MTPROTO прокси: {settings.PROXY_ADDR}:{settings.PROXY_PORT}")
    
    if not hasattr(settings, 'PROXY_SECRET') or not settings.PROXY_SECRET:
        print("⚠️ PROXY_SECRET не найден, пробуем без secret")
        proxy_string = f"socks5h://{settings.PROXY_ADDR}:{settings.PROXY_PORT}"
    else:
        secret = settings.PROXY_SECRET
        print(f"🔑 Используем secret: {secret[:10]}...")
        
        # Пробуем разные форматы
        proxy_variants = [
            f"socks5h://{secret}@{settings.PROXY_ADDR}:{settings.PROXY_PORT}",  # secret как логин
            f"socks5h://:{secret}@{settings.PROXY_ADDR}:{settings.PROXY_PORT}", # secret как пароль
            f"socks5h://{settings.PROXY_ADDR}:{settings.PROXY_PORT}"  # без secret
        ]
        
        # Пробуем каждый вариант
        for i, proxy_str in enumerate(proxy_variants):
            print(f"🔄 Пробуем вариант {i+1}: {proxy_str[:30]}...")
            apihelper.proxy = {'https': proxy_str}
            
            # Создаем временного бота для теста
            test_bot = telebot.TeleBot(settings.TOKEN)
            try:
                me = test_bot.get_me()
                print(f"✅ Вариант {i+1} работает! Бот: @{me.username}")
                return proxy_str
            except:
                print(f"❌ Вариант {i+1} не работает")
                continue
        
        print("❌ Ни один вариант не подошел")
        return None

# Настраиваем прокси
proxy_string = setup_mtproto_proxy()

# Создаем бота с последним удачным вариантом
if proxy_string:
    apihelper.proxy = {'https': proxy_string}
else:
    print("⚠️ Запускаем без прокси")
    apihelper.proxy = None

bot = telebot.TeleBot(settings.TOKEN)

# Проверка
try:
    me = bot.get_me()
    print(f"✅ Бот @{me.username} запущен!")
except Exception as e:
    print(f"❌ Ошибка: {e}")


def setup_mtproto_proxy():
    print(f"🔄 Настройка MTPROTO прокси: {settings.PROXY_ADDR}:{settings.PROXY_PORT}")
    
    # Базовые настройки прокси
    proxy_dict = {
        'proxy_type': 'socks5',  # или socks.SOCKS5H если нужно разрешение DNS через прокси
        'addr': settings.PROXY_ADDR,
        'port': settings.PROXY_PORT,
        'username': None,
        'password': None
    }
    
    # Если есть секрет, пробуем использовать его как username
    if hasattr(settings, 'PROXY_SECRET') and settings.PROXY_SECRET:
        print(f"🔑 Используем secret: {settings.PROXY_SECRET[:10]}...")
        proxy_dict['username'] = settings.PROXY_SECRET
        # Некоторые прокси требуют password вместо username
        # proxy_dict['password'] = settings.PROXY_SECRET
    
    # Тестируем прокси
    apihelper.proxy = proxy_dict
    test_bot = telebot.TeleBot(settings.TOKEN)
    
    try:
        me = test_bot.get_me()
        print(f"✅ Прокси работает! Бот: @{me.username}")
        return proxy_dict
    except Exception as e:
        print(f"❌ Прокси не работает: {e}")
        
        # Пробуем без прокси
        print("🔄 Пробуем без прокси...")
        apihelper.proxy = None
        try:
            me = test_bot.get_me()
            print(f"✅ Бот работает без прокси! Бот: @{me.username}")
            return None
        except:
            print("❌ Бот не работает даже без прокси")
            return None

# Настраиваем прокси
proxy_config = setup_mtproto_proxy()

# Применяем настройки
if proxy_config:
    apihelper.proxy = proxy_config
else:
    apihelper.proxy = None


PROXY = f'{settings.PROXY_SECRET}:None@{settings.PROXY_ADDR}:{settings.PROXY_PORT}'

apihelper.proxy = {'https':'socks5h://' + PROXY}
"""


bot = telebot.TeleBot(settings.TOKEN)


openaiapi = settings.OPENAI

catalog_ya = settings.CATALOG_ID
ya_api = settings.Y_Api_Key