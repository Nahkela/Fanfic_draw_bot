from aiogram import Router
from lexicon.lexicon import LEXICON_RU
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from filters.filters import IsInBase

router = Router()


# Приветствие с пользованием, маленькое представление, что из себя представляет бот
@router.message(CommandStart(), IsInBase(False))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['start'])


# Описание команд бота, более подробное объяснение
@router.message(Command(commands='help'))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['help'])

