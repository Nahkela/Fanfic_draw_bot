from aiogram.filters import BaseFilter
from aiogram.types import Message

user_ids: dict[int, dict[str, list[str] | int]] = {}
user_conditions = {}
states: dict[str, [int, list]] = {'names_count': 2, 'get_name': 0, 'conditions_count': 0, 'conditions': [],
                                  'accepted_count_condition': 2}


class IsInBase(BaseFilter):
    def __init__(self, user_ids):
        self.user_ids = user_ids

    async def __call__(self, message: Message):
        return message.from_user.id not in self.user_ids.keys()


class MoreInBase(BaseFilter):
    def __init__(self, user_ids):
        self.user_ids = user_ids

    async def __call__(self, message: Message):
        return message.from_user.id in self.user_ids.keys() and len(self.user_ids[message.from_user.id]['own_names']) == 2


class NamesDone(BaseFilter):
    def __init__(self, names_count):
        self.names_count = names_count

    async def __call__(self, message: Message):
        return self.names_count < states['names_count']


class WriteAbility(BaseFilter):
    def __init__(self, user_ids, count):
        self.user_ids = user_ids
        self.count = count

    async def __call__(self, message: Message):
        return len(self.user_ids[message.from_user.id]['own_conditions']) < self.count
