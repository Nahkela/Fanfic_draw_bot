from aiogram.filters import BaseFilter
from aiogram.types import Message
from Base.Base import states, user_db
from lexicon.lexicon import LEXICON_RU


class DickWriter:
    def __init__(self, function):
        self.function = function
        self.text = ''

    def __call__(self, *args):
        for key, value in self.function(*args).items():
            self.text += f"{LEXICON_RU[key]}:\n{' '*4}"
            if key == 'victim':
                self.text += f'{user_db[value]["name"]}\n'
                continue
            if key == 'conditions':
                self.text += f'{"; ".join(value)}\n'
            else:
                self.text += f'{", ".join([LEXICON_RU[val] for val in value])}\n'
        text = self.text
        self.text = ''
        return text


class RegisterTry(BaseFilter):

    async def __call__(self, message: Message):
        return message.text != '/register'


class IsInBase(BaseFilter):
    def __init__(self, mode=True):
        self.user_ids = user_db
        self.mode = mode

    async def __call__(self, message: Message):
        if self.mode is True:
            return message.from_user.id in self.user_ids.keys()
        else:
            return message.from_user.id not in self.user_ids.keys()


class WriteAbility(BaseFilter):
    def __init__(self, user_ids, count):
        self.user_ids = user_ids
        self.count = count

    async def __call__(self, message: Message):
        return len(self.user_ids[message.from_user.id]['own_conditions']) < self.count

