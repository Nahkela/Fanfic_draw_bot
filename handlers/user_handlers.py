from aiogram.types import Message
from aiogram.filters import CommandStart, Text
from aiogram import Router, F
from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import start_keyboard, names_keyboard
from Base.Base import user_ids, IsInBase, MoreInBase, states, NamesDone
from services.services import choose_victim


router = Router()
router.message.filter(NamesDone(states['get_name']))


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=start_keyboard)


@router.message(Text(text=LEXICON_RU['agree_button']))
async def process_agree_command(message: Message):
    await message.answer(text=LEXICON_RU['get_own_name'], reply_markup=names_keyboard)


@router.message(Text(text=LEXICON_RU['disagree_button']))
async def process_disagree_command(message: Message):
    await message.answer(text=LEXICON_RU['disagree'])


@router.message(Text(text=LEXICON_RU['names']), MoreInBase(user_ids))
async def process_hitrozhop_command(message: Message):
    await message.answer(text=LEXICON_RU['Many_tries'])


@router.message(Text(text=LEXICON_RU['names']), IsInBase(user_ids))
async def process_own_name_command(message: Message):
    user_ids.setdefault(message.from_user.id, {})
    user_ids[message.from_user.id].setdefault('own_names', []).append(message.text)
    print(user_ids[message.from_user.id]['own_names'][0])
    await message.answer(text=LEXICON_RU['get_last_name'], reply_markup=names_keyboard)


@router.message(Text(text=LEXICON_RU['names']))
async def process_other_name_command(message: Message):
    user_ids[message.from_user.id].setdefault('own_names', []).append(message.text)
    victim = choose_victim(LEXICON_RU['already_chosen'], user_ids[message.from_user.id]['own_names'], LEXICON_RU['names'])
    states['get_name'] += 1
    user_ids[message.from_user.id].setdefault('own_conditions', [])
    user_ids[message.from_user.id].setdefault('got_conditions', [])
    print(states['get_name'])
    print(states['get_name'] < states['names_count'])
    await message.answer(text=f"{LEXICON_RU['finally']}: {victim}\n"
                              f"Теперь напиши условия, одним сообщением\n"
                              f"Отменять пока не умею, так что го без ошибок пока что")
