from dataclasses import dataclass

from environs import Env


@dataclass
class TelegramBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TelegramBot


def load_config(path: str or None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TelegramBot(
        token=env("BOT_TOKEN"),
        admin_ids=list(map(int, env.list("ADMIN_IDS")))
    ))