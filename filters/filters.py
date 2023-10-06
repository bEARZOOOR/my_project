from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import load_config, Config


config: Config = load_config()


bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()
admin_ids:list[int] = config.tg_bot.admin_ids


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids:list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
    