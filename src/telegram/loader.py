from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from src.adapters.redis import redis
from src.core.config import settings

bot = Bot(
    token=settings.telegram.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)
storage = RedisStorage(redis)
dispatcher = Dispatcher(bot=bot, storage=storage)
