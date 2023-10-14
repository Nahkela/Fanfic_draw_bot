from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.context import FSMContext
from FSMClasses.fsmclasses import FSMFillform
from lexicon.lexicon import LEXICON_RU
from filters.fsmfilters import is_name_correct, is_age_correct
from keyboards.kb_maker import inline_keyboard_maker
from Base.Base import user_db
from filters.filters import IsInBase, RegisterTry

router = Router()
router.message.filter(IsInBase(False))


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте команду /register'
    )


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /register'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Регистрация пользователя, вхождение в машину состояний, заполнение анкеты
@router.message(Command(commands='register'), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['register'])
    # Переход к состоянию заполнению анкеты, заполнение начинается с имени
    await state.set_state(FSMFillform.fill_name)


# Хэндлер для апдейта имени, если имя введено корректно
@router.message(StateFilter(FSMFillform.fill_name), lambda x: is_name_correct(x.text))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['filled_name'])
    await state.update_data(name=message.text)
    # Переход к состоянию заполнения возраста
    await state.set_state(FSMFillform.fill_age)


# Хэндлер если имя введено не корректно
@router.message(StateFilter(FSMFillform.fill_name))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['filled_name_false'])


# Хендлер для апдейта возраста, если возраст введён корректно
@router.message(StateFilter(FSMFillform.fill_age), lambda x: is_age_correct(x.text))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['filled_age'],
                         reply_markup=inline_keyboard_maker(2, 'male', 'female', 'undefined_gender'))
    await state.update_data(age=message.text)
    # Переход к состоянию заполнения пола
    await state.set_state(FSMFillform.fill_gender)


# Хэндлер если возраст введен не корректно
@router.message(StateFilter(FSMFillform.fill_age))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['filled_age_false'])


# Хэндлер для апдейта пола, если был выбран среди инлайн кнопок
@router.callback_query(StateFilter(FSMFillform.fill_gender), F.data.in_(['male', 'female', 'undefined_gender']))
async def process_start_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RU['filled_gender'])
    await callback.answer()
    await state.update_data(gender=LEXICON_RU[callback.data])
    # Переход к состоянию загрузки фото
    await state.set_state(FSMFillform.upload_photo)


# Хэндлер если гендер был выбран не среди кнопок
@router.message(StateFilter(FSMFillform.fill_gender))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['filled_gender_false'])


# Хэндлер если было загружено фото
@router.message(StateFilter(FSMFillform.upload_photo), F.photo[-1].as_('largest_photo'))
async def process_start_command(message: Message, state: FSMContext, largest_photo: PhotoSize):
    await state.update_data(
        photo_id=largest_photo.file_id,
        photo_unique_id=largest_photo.file_unique_id
    )
    time_dick = await state.get_data()   # Получаем данные с машины состояний
    user_db.setdefault(message.from_user.id, {}).update(time_dick)# Обновляем наш словарь юзера
    user_db[message.from_user.id].update({'modes': {}})
    await message.answer(text=LEXICON_RU['uploaded_photo'])
    await state.clear()


# Хэндлер если было загружено не фото
@router.message(StateFilter(FSMFillform.upload_photo))
async def process_start_command(message: Message, state):
    await message.answer(text=LEXICON_RU['uploaded_photo_fail'])


# Для тех, кто хочет сделать что-либо до регистрации
@router.message()
async def process_register_warning_command(message: Message):
    await message.answer(text=LEXICON_RU['register_warning'])
