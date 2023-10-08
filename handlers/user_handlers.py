from aiogram.types import Message
from aiogram.filters import CommandStart, Text, Command
from aiogram import Router, F
from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import start_keyboard, names_keyboard
from Base.Base import user_ids
from filters.filters import IsInBase, MoreInBase, states, NamesDone
from services.services import choose_victim


router = Router()
router.message.filter(NamesDone(states['get_name']))


@router.message(Command(commands='player_draw'))
async def process_start_command(message: Message):
    pass
