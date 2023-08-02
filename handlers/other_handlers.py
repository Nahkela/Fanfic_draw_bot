from aiogram.types import Message
from aiogram import Router
from lexicon.lexicon import LEXICON_RU

router = Router()


@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_RU['other_messages'])


