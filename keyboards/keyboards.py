from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU


#Создаём клавиатуру на начальный вопрос про жеребьёвку
yes_button: KeyboardButton = KeyboardButton(text=LEXICON_RU['agree_button'])
no_button: KeyboardButton = KeyboardButton(text=LEXICON_RU['disagree_button'])

yes_no_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
yes_no_builder.row(yes_button, no_button, width=2)
start_keyboard: ReplyKeyboardMarkup = yes_no_builder.as_markup(one_time_keyboard=True,
                                                               resize_keyboard=True)

name_buttons: list[KeyboardButton] = [KeyboardButton(text=name) for name in LEXICON_RU['names']]

name_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
name_kb_builder.row(*name_buttons, width=3)
names_keyboard: ReplyKeyboardMarkup = name_kb_builder.as_markup(resize_keyboard=True,
                                                                one_time_keyboard=True)

conditions_button: KeyboardButton = KeyboardButton(text=LEXICON_RU['get_conditions_button'])
conditions_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[conditions_button]], resize_keyboard=True)
