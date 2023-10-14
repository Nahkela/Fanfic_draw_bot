from random import choice, randint
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


def choose_victim(victims: list, own_names: list, names: list) -> str:
    variants = [name for name in names if name not in victims and name not in own_names]
    goal = choice(variants)
    victims.append(goal)
    return goal


def key_generator():
    return f"{randint(1, 99):02}{randint(1, 99):02}{randint(1, 99):02}{randint(1, 99):02}"



