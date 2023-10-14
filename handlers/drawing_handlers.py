from copy import deepcopy
from aiogram import Router, F
from lexicon.lexicon import LEXICON_RU
from Base.Base import user_db, draw_rooms, states, draw_rooms_story
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from keyboards.kb_maker import inline_keyboard_maker
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FSMClasses.fsmclasses import FSMInitDrawing
from services.services import key_generator
from aiogram import Bot


router = Router()


@router.message(Command(commands='drawing'), StateFilter(default_state))
async def process_start_drawing_command(message: Message, state: FSMContext):
    print(message.chat.id)
    user_db[message.from_user.id]['modes']['drawing'] = {'is_drawing': True,
                                                         'is_initiator': False,
                                                         'time_id_key': False
                                                         }
    await message.answer(text=LEXICON_RU['start_drawing'],
                         reply_markup=inline_keyboard_maker(
                             4,
                             'initiator',
                             'guest'
                         ))
    await state.set_state(FSMInitDrawing.draw_started)


# Обработка нажатия на кнопку Инициатор, предложение количества жанров
@router.callback_query(F.data == 'initiator', StateFilter(FSMInitDrawing.draw_started))
async def process_initiator_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_RU['fill_genre_count'],
        reply_markup=inline_keyboard_maker(3, '1', '2', '3', 'no_genre')
    )
    while True:
        key = key_generator()
        if key not in draw_rooms_story:
            draw_rooms_story[key] = {}
            break
    await state.update_data(key=key)
    draw_rooms[key] = deepcopy(states)
    draw_rooms[key].update({'owner': callback.from_user.id})
    user_db[callback.from_user.id]['modes']['drawing']['is_initiator'] = True
    user_db[callback.from_user.id]['modes']['drawing']['time_id_key'] = key

    await state.set_state(FSMInitDrawing.fill_genres_count)
    await callback.answer()


@router.callback_query(StateFilter(FSMInitDrawing.draw_started), F.data == 'guest')
async def process_guest_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['guest_begin'])
    await callback.message.delete()
    await state.set_state(FSMInitDrawing.fill_guest_key)


@router.message(StateFilter(FSMInitDrawing.draw_started))
async def process_initiator_command(message: Message, state: FSMContext):
    await message.answer(text='НА КНОПКУУУУ')


@router.message(StateFilter(FSMInitDrawing.fill_guest_key), lambda x: x.text.isdigit())
async def process_guest_key_command(message: Message, state: FSMContext, bot: Bot):
    if message.text not in draw_rooms:
        await message.answer(text=LEXICON_RU['no_key'])
    else:
        await state.update_data(key=message.text)
        draw_rooms[message.text]['play_ids'].add(message.from_user.id)
        print(draw_rooms[message.text]['time_requit_message_id'])
        await bot.edit_message_text(text=f"{LEXICON_RU['stop_recruitment']}{len(draw_rooms[message.text]['play_ids'])}",
                                    message_id=draw_rooms[message.text]['time_requit_message_id'],
                                    chat_id=draw_rooms[message.text]['time_requit_chat_id'],
                                    reply_markup=inline_keyboard_maker(1, 'stop_recruitment_button')
                                    )
        await message.answer(text=LEXICON_RU['now_wait'])


@router.message(StateFilter(FSMInitDrawing.fill_guest_key))
async def process_fail_fill_key_command(message: Message):
    await message.answer(text=LEXICON_RU['only_digits'])


# Запись количества жанра и переход с вопросом об условиях
@router.callback_query(StateFilter(FSMInitDrawing.fill_genres_count), F.data.in_(['1', '2', '3', 'no_genre']))
async def process_genres_sent(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_RU['chosen_genres_count'],
        reply_markup=inline_keyboard_maker(3, '1', '2', '3', 'no_condions')
    )
    # Увы, по другому забрать по ключу 'key' не получится, так что вот надо так страдать
    # из кода в код, что поделать. Хотя может просто я тупой
    room_key = await state.get_data()
    # По ключу комнаты в бд инициатора находим комнату и затем меняем там данные о жанрах
    # записываем количество жанров, либо False, если их нет
    draw_rooms[room_key['key']]['genres_counts'] = int(callback.data) if callback.data.isdigit() else False
    await state.set_state(FSMInitDrawing.fill_conditions_count)
    await callback.answer()


# Если нажмут не на кнопку
@router.message(StateFilter(FSMInitDrawing.fill_genres_count))
async def process_genres_sent(message: Message, state: FSMContext):
    await message.answer(
        text='Следуйте кнопкам')


# Заполнение данных о количестве условий и переход к набору игроков
@router.callback_query(StateFilter(FSMInitDrawing.fill_conditions_count), F.data.in_(['1', '2', '3', 'no_conditions']))
async def process_genres_sent(callback: CallbackQuery, state: FSMContext):
    room_key = await state.get_data()

    # Записываем ID сообщения, чтоб потом изменять его текст позже, правда это должно быть сделано не здесь так-то
    draw_rooms[room_key['key']]['time_requit_message_id'] = callback.message.message_id
    draw_rooms[room_key['key']]['time_requit_chat_id'] = callback.message.chat.id
    # записываем количество условий, либо False, если их нет
    draw_rooms[room_key['key']]['conditions_counts'] = int(callback.data) if callback.data.isdigit() else False
    await callback.message.edit_text(text=f"{LEXICON_RU['key'].title()}: {room_key['key']}\n"
                                          f"{LEXICON_RU['chosen_conditions_count']}\n"
                                          f"{LEXICON_RU['stop_recruitment']}",
                                     reply_markup=inline_keyboard_maker(1, 'stop_recruitment_button')
                                     )
    await state.set_state(FSMInitDrawing.stop_requit)


@router.message(StateFilter(FSMInitDrawing.fill_conditions_count))
async def process_genres_sent(message: Message):
    await message.answer(
        text='Нажми на существующую кнопку ради всего святого')


# Позже надо сделать создать класса фильтра, который передаёт данные в хендлер, если данные из какого-либо списка
# есть в апдейте, убирать из списка после обработки, это будет заменой генератора хендлеров


@router.callback_query(StateFilter(FSMInitDrawing.stop_requit), F.data == 'stop_recruitment_button')
async def process_stop_requit_command(callback: CallbackQuery, bot: Bot, state: FSMContext):
    room_key = await state.get_data()
    keyboard = inline_keyboard_maker(3, *draw_rooms[room_key['key']]['play_ids'])
    if draw_rooms[room_key['key']]['play_ids']:
        await callback.message.edit_text(text=LEXICON_RU['begin_main_drawing'],
                                         reply_markup=keyboard)
        for user in draw_rooms[room_key['key']]['play_ids']:
            await bot.send_message(text=LEXICON_RU['begin_main_drawing'],
                                   chat_id=user,
                                   reply_markup=keyboard
                                   )
            await callback.answer()
    else:
        await callback.answer(text='Пока что кроме вас никого нет')



