"""Заглушки внешних зависимостей для тестов.

Оба набора тестов используют один набор заглушек: если каждый подменит
sys.modules по-своему, один тест перетрёт заглушки другого и тот упадёт
с ImportError, не связанным с реальной ошибкой кода.
"""

import sys
import types
from pathlib import Path

# Каталог tdm_bot в sys.path — импорты в проекте абсолютные
BOT_ROOT = Path(__file__).resolve().parent.parent
if str(BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(BOT_ROOT))

# Имена, которые бот импортирует из messenger_bot_api
MESSENGER_NAMES = [
    'Application', 'BotEvent', 'MessageBotEvent', 'MessageUpdateBotEvent',
    'MessageDeleteBotEvent', 'MessagesDeleteBotEvent',
    'MessagesDeletedCompletelyBotEvent', 'GroupUserRemoveBotEvent',
    'GroupMeRemoveBotEvent', 'GroupUserLeaveBotEvent', 'GroupUsersAddBotEvent',
    'GroupUserJoinBotEvent', 'GroupMeAddBotEvent',
    'UserSignedUpToWorkspaceBotEvent', 'HistoryClearGroupBotEvent',
    'DeleteGroupBotEvent', 'UserUpdateBotEvent', 'Handler', 'EventHandler',
    'MessageHandler', 'CommandHandler', 'DeleteMessageEventHandler',
    'DeleteMessagesEventHandler', 'UpdateMessageEventHandler',
    'GroupUserJoinHandler', 'GroupUsersAddHandler', 'GroupUserLeaveHandler',
    'GroupUserRemoveHandler', 'GroupMeAddHandler', 'GroupMeRemoveHandler',
    'GroupHistoryClearHandler', 'GroupDeleteHandler',
    'UserSignedUpToWorkspaceHandler', 'UserUpdateHandler',
    'MessagesDeletedCompletelyHandler', 'FormattingSettings', 'TextMarkups',
    'TextUrlMarkup', 'TextMarkup', 'ClickButtonEventHandler',
    'InlineMessageButton', 'SelectedButton', 'MessageRequest', 'Image',
    'File', 'Video', 'InvalidInviteLinkException', 'FileUploadException',
]


def _pandas_stub():
    """Минимальный pandas: тестам нужен только факт импорта,
    реальные запросы идут через psycopg2, а не через DataFrame"""
    module = types.ModuleType('pandas')

    class DataFrame:
        shape = (0, 0)
        loc = None
        iloc = None

        def __getitem__(self, item):
            return self

        def __len__(self):
            return 0

        def drop_duplicates(self, **kwargs):
            return self

        def reset_index(self, **kwargs):
            return self

        def iterrows(self):
            return iter(())

        def to_dict(self):
            return {}

    class Series:
        pass

    module.DataFrame = DataFrame
    module.Series = Series
    module.isna = lambda value: False
    return module


def install():
    """Установка всех заглушек. Идемпотентна: повторный вызов безопасен."""
    sys.modules['pandas'] = _pandas_stub()

    psycopg2 = types.ModuleType('psycopg2')
    psycopg2.connect = lambda **kwargs: None
    psycopg2.extensions = types.ModuleType('psycopg2.extensions')
    sys.modules['psycopg2'] = psycopg2

    settings = types.ModuleType('settings')
    settings.DB_PROD_HOST = 'localhost'
    settings.DB_PROD_DATABASE = 'supra_sport'
    settings.DB_PROD_NAME = 'supra_sport'
    settings.DB_PROD_PASSWORD = 'secret'
    settings.TOKEN = 'BOT-test-token'
    settings.REST = 'https://api.tdm.mos.ru'
    settings.SSE = 'https://pusher.tdm.mos.ru'
    settings.FILE = 'https://fileupload.tdm.mos.ru'
    sys.modules['settings'] = settings

    messenger = types.ModuleType('messenger_bot_api')

    # File/Image/Video — ресурсы, которые конструируются как File(name, data)
    # и хранят .name/.content. Остальным именам достаточно пустого класса.
    def _resource_init(self, name=None, content=None):
        self.name = name
        self.content = content

    resource = type('Resource', (), {'__init__': _resource_init})
    for name in ('File', 'Image', 'Video'):
        setattr(messenger, name, type(name, (resource,), {}))

    for name in MESSENGER_NAMES:
        if not hasattr(messenger, name):
            setattr(messenger, name, type(name, (), {}))
    messenger.__all__ = list(MESSENGER_NAMES)
    sys.modules['messenger_bot_api'] = messenger


install()