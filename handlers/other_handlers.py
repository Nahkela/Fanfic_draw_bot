from aiogram import Router
from lexicon.lexicon import LEXICON_RU
from Base.Base import user_db
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

router = Router()


@router.message(Command(commands='showdata'))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_db:
        await message.answer_photo(
            photo=user_db[message.from_user.id]['photo_id'],
            caption=f'Имя: {user_db[message.from_user.id]["name"]}\n'
                    f'Возраст: {user_db[message.from_user.id]["age"]}\n'
                    f'Пол: {user_db[message.from_user.id]["gender"]}\n'
        )

    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли анкету. Чтобы приступить - '
            'отправьте команду /register'
        )


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['start_false'])


@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_RU['other_messages'])


@router.callback_query()
async def send_answer(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['other_messages'])
    await callback.answer()


