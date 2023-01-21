from dotenv import load_dotenv
from os import getenv
from telethon.client import TelegramClient

load_dotenv()


class Settings:
    SESSION_TYPE = getenv('SESSION_TYPE')
    IS_PROD = SESSION_TYPE == 'PROD'
    API_ID = getenv(f'API_ID_{SESSION_TYPE}')
    API_HASH = getenv(f'API_HASH_{SESSION_TYPE}')
    BOT_TOKEN = getenv(f'BOT_TOKEN_{SESSION_TYPE}')
    client = None

    @classmethod
    async def get_client(cls) -> TelegramClient:
        if cls.client is None:
            cls.client = await TelegramClient(
                f'fu_{cls.SESSION_TYPE.lower()}',
                cls.API_ID,
                cls.API_HASH
            ).start(bot_token=cls.BOT_TOKEN)

        return cls.client