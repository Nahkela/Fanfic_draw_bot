from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


def inline_keyboard_maker(width, *args) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    if args:
        for name in args:
            buttons.append(
                InlineKeyboardButton(
                    text=LEXICON_RU[name] if name in LEXICON_RU else name,
                    callback_data=name
                )
            )
    kb_builder.row(*buttons)
    return kb_builder.as_markup(width=width)
