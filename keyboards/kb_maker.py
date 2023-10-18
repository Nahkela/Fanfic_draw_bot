from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


def inline_keyboard_maker(width, *args, **kwargs) -> InlineKeyboardMarkup:
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
    if kwargs:
        for callback, name in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=name,
                callback_data=callback
            ))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()

