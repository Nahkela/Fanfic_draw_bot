from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


class DataBase:
    def __init__(self, names=None):
        if names is None:
            self.names: dict = {}


@dataclass
class Config:
    tg_bot: TgBot
    database: DataBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), database=DataBase())

