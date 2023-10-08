from environs import Env
from dataclasses import dataclass
from aiogram.fsm.storage.memory import MemoryStorage


@dataclass
class TgBot:
    token: str


class DataBase:
    def __init__(self, names=None):
        if names is None:
            self.names: dict = {}
        self.storage = MemoryStorage()


@dataclass
class Config:
    tg_bot: TgBot
    database: DataBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), database=DataBase())

