from copy import deepcopy
from aiogram import Router, F, Bot
from lexicon.lexicon import LEXICON_RU, LEXICON_GENRES
from Base.Base import user_db, draw_rooms, states, draw_rooms_story, drawing_options, all_genres
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter, or_f
from keyboards.kb_maker import inline_keyboard_maker
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FSMClasses.fsmclasses import FSMInitDrawing
from services.services import key_generator, generate
from aiogram.exceptions import TelegramBadRequest


router = Router()


@router.message(Command(commands='drawing'), StateFilter(default_state))
async def process_start_drawing_command(message: Message, state: FSMContext):
    await state.clear()
    user_db[message.from_user.id]['modes']['drawing'] = deepcopy(drawing_options)
    user_db[message.from_user.id]['last_callback'] = await message.answer(text=LEXICON_RU['start_drawing'],
                         reply_markup=inline_keyboard_maker(
                             4,
                             'initiator',
                             'guest'
                         ))
    await state.set_state(FSMInitDrawing.draw_started)

router.message(lambda x: user_db[x.from_user.id]['drawing'])


@router.message(Command(commands='cancel_draw'), ~StateFilter(FSMInitDrawing.wait,
                                                              FSMInitDrawing.draw_started,
                                                              FSMInitDrawing.fill_guest_key,
                                                              FSMInitDrawing.fill_genres_count,
                                                              FSMInitDrawing.fill_conditions_count),
                lambda x: len(draw_rooms[user_db[x.from_user.id]['room_id']]['play_ids']) - 1 <= 1)
async def process_cancel_draw_command_3(message: Message, state: FSMContext, bot: Bot):
    room = await state.get_data()
    for user in draw_rooms[room['key']]['play_ids']:
        try:
            await user_db[user]['last_callback'].delete()
        except (TelegramBadRequest, KeyError, AttributeError):
            print('Удалять нечего')
        await bot.send_message(text=LEXICON_RU['empty_room'],
                               chat_id=user)
        user_db[user]['modes']['drawing'] = False
    del draw_rooms[room['key']]
    await state.clear()


@router.message(Command(commands='cancel_draw'), StateFilter(FSMInitDrawing.wait))
async def process_cancel_draw_command_3(message: Message, state: FSMContext, bot: Bot):
    room = await state.get_data()
    user_db[message.from_user.id]['modes']['drawing'] = False
    draw_rooms[room['key']]['play_ids'].discard(message.from_user.id)
    user_db[draw_rooms[room['key']]['owner']]['last_callback'] = await bot.edit_message_text(
                                        text=f"{LEXICON_RU['stop_recruitment']}{len(draw_rooms[room['key']]['play_ids'])+1}",
                                        message_id=user_db[draw_rooms[room['key']]['owner']]['last_callback'].message_id,
                                        chat_id=draw_rooms[room['key']]['owner'],
                                        reply_markup=inline_keyboard_maker(1, 'stop_recruitment_button')
                                                                                 )
    await message.answer(text='AAAAA')


@router.message(Command(commands='cancel_draw'), StateFilter(FSMInitDrawing.the_end))
async def process_cancel_draw_command(message: Message, state: FSMContext):
    room = await state.get_data()
    await message.answer(LEXICON_RU['too_late'])
    await draw_rooms[room['key']]['over'].add(message.from_user.id)


@router.message(Command(commands='cancel_draw'), StateFilter(FSMInitDrawing.fill_guest_key,
                                                             FSMInitDrawing.fill_genres_count,
                                                             FSMInitDrawing.fill_conditions_count),
                lambda x: user_db[x.from_user.id]['modes']['drawing']['is_initiator'])
async def process_cancel_draw_command_1(message: Message, state: FSMContext):
    try:
        await user_db[message.from_user.id]['last_callback'].delete()
    except (TelegramBadRequest, KeyError, AttributeError):
        print('Удалять нечего')
    user_db[message.from_user.id]['modes']['drawing'] = False
    room = await state.get_data()
    del draw_rooms[room['key']]
    await state.set_state(default_state)
    await message.answer(text=LEXICON_RU['draw_exit'])


@router.message(Command(commands='cancel_draw'), ~StateFilter(default_state))
async def process_cancel_draw_command_2(message: Message, state: FSMContext, bot: Bot):
    try:
        await user_db[message.from_user.id]['last_callback'].delete()
    except (TelegramBadRequest, KeyError, AttributeError):
        print('Удалять нечего')
    room_key = await state.get_data()
    if 'key' in room_key:
        betrayer = message.from_user.id
        draw_rooms[room_key['key']]['play_ids'].discard(message.from_user.id)
        for user in draw_rooms[room_key['key']]['play_ids']:
            await bot.send_message(text=f"{user_db[betrayer]['name']}{' betrayed us'}",
                                   chat_id=user)

        user_db[message.from_user.id]['modes']['drawing'] = False

    await message.answer(LEXICON_RU['draw_exit'])
    await state.set_state(default_state)


# Обработка нажатия на кнопку Инициатор, предложение количества жанров
@router.callback_query(F.data == 'initiator', StateFilter(FSMInitDrawing.draw_started))
async def process_initiator_command(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['state'] = state
    user_db[callback.from_user.id]['last_callback'] = await callback.message.edit_text(
        text=LEXICON_RU['fill_genre_count'],
        reply_markup=inline_keyboard_maker(3, '1', '2', '3', 'no_genre')
    )
    while True:
        key = key_generator()
        if key not in draw_rooms_story:
            draw_rooms_story[key] = {}
            break
    await state.update_data(key=key)
    user_db[callback.from_user.id]['room_id'] = key
    draw_rooms[key] = deepcopy(states)
    draw_rooms[key]['owner'] = callback.from_user.id
    user_db[callback.from_user.id]['modes']['drawing']['is_initiator'] = True
    user_db[callback.from_user.id]['modes']['drawing']['time_id_key'] = key
    user_db[callback.from_user.id]['modes']['drawing']['genres'] = deepcopy([genre for genre in all_genres])
    await state.set_state(FSMInitDrawing.fill_genres_count)
    await callback.answer()


@router.callback_query(StateFilter(FSMInitDrawing.draw_started), F.data == 'guest')
async def process_guest_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['guest_begin'])
    await callback.message.delete()
    await state.set_state(FSMInitDrawing.fill_guest_key)


@router.message(StateFilter(FSMInitDrawing.draw_started))
async def process_initiator_command(message: Message):
    await message.answer(text='НА КНОПКУУУУ, либо выйдете из режима жеребьёвки, используя /cancel_draw')


@router.message(StateFilter(FSMInitDrawing.fill_guest_key), lambda x: x.text.isdigit())
async def process_guest_key_command(message: Message, state: FSMContext, bot: Bot):
    if message.text not in draw_rooms:
        await message.answer(text=LEXICON_RU['no_key'])
    else:
        await state.update_data(key=message.text)
        draw_rooms[message.text]['play_ids'].add(message.from_user.id)
        user_db[message.from_user.id]['last_callback'] = await bot.edit_message_text(text=f"{LEXICON_RU['stop_recruitment']}{len(draw_rooms[message.text]['play_ids'])+1}",
                                    message_id=draw_rooms[message.text]['time_requit_message_id'],
                                    chat_id=draw_rooms[message.text]['time_requit_chat_id'],
                                    reply_markup=inline_keyboard_maker(1, 'stop_recruitment_button')
                                    )
        await message.answer(text=LEXICON_RU['now_wait'])
        # Ужасный костыль, в будущем состояние stop_requit будет работать для двух хендлеров на двух этапах
        # спасает то, что и там и там CallbackQuery, Просто главный бот передаёт всем сообщений с инлайн кнопками,
        # но не может всем изменить их состояния, в будущем мб изменю систему.
        # Изменил, осталась проблема отмены жеребьёвки в режиме набора команды.
        user_db[message.from_user.id]['state'] = state
        await state.set_state(FSMInitDrawing.wait)


@router.message(StateFilter(FSMInitDrawing.fill_guest_key))
async def process_fail_fill_key_command(message: Message):
    await message.answer(text=LEXICON_RU['only_digits'])


# Запись количества жанра и переход с вопросом об условиях
@router.callback_query(StateFilter(FSMInitDrawing.fill_genres_count), F.data.in_(['1', '2', '3', 'no_genre']))
async def process_genres_sent(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['last_callback'] = await callback.message.edit_text(
        text=LEXICON_RU['chosen_genres_count'],
        reply_markup=inline_keyboard_maker(3, '1', '2', '3', 'no_conditions')
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
async def process_genres_sent(message: Message):
    await message.answer(
        text='Следуйте кнопкам, либо выйдете из режима жеребьёвки, используя /cancel_draw')


# Заполнение данных о количестве условий и переход к набору игроков
@router.callback_query(StateFilter(FSMInitDrawing.fill_conditions_count), F.data.in_(['1', '2', '3', 'no_conditions']))
async def process_genres_sent(callback: CallbackQuery, state: FSMContext):
    room_key = await state.get_data()

    # Записываем ID сообщения, чтоб потом изменять его текст позже, правда это должно быть сделано не здесь так-то
    draw_rooms[room_key['key']]['time_requit_message_id'] = callback.message.message_id
    draw_rooms[room_key['key']]['time_requit_chat_id'] = callback.message.chat.id
    # записываем количество условий, либо False, если их нет
    draw_rooms[room_key['key']]['conditions_counts'] = int(callback.data) if callback.data.isdigit() else False

    user_db[callback.from_user.id]['last_callback'] = await callback.message.edit_text(
                                    text=f"{LEXICON_RU['key'].title()}: {room_key['key']}\n"
                                         f"{LEXICON_RU['chosen_conditions_count']}\n"
                                         f"{LEXICON_RU['stop_recruitment']}",
                                    reply_markup=inline_keyboard_maker(1, 'stop_recruitment_button')
                                    )
    await state.set_state(FSMInitDrawing.stop_requit)


@router.message(StateFilter(FSMInitDrawing.fill_conditions_count))
async def process_genres_sent(message: Message):
    await message.answer(
        text='Нажми на существующую кнопку ради всего святого,\n'
             'Либо выйдете из режима жеребьёвки, используя /cancel_draw')


# Позже надо сделать создать класса фильтра, который передаёт данные в хендлер, если данные из какого-либо списка
# есть в апдейте, убирать из списка после обработки, это будет заменой генератора хендлеров


@router.callback_query(StateFilter(FSMInitDrawing.stop_requit), F.data == 'stop_recruitment_button')
async def process_stop_requit_command(callback: CallbackQuery, bot: Bot, state: FSMContext):
    room = await state.get_data()
    if draw_rooms[room['key']]['play_ids']:
        await state.update_data(players_id=list(draw_rooms[room['key']]['play_ids']))
        await callback.message.delete()
        draw_rooms[room['key']]['play_ids'].add(callback.from_user.id)
        keyboard = inline_keyboard_maker(3, **{str(x[0]): x[1] for x in map(lambda x: (x, user_db[x]['name']), draw_rooms[room['key']]['play_ids'])})

        for user in draw_rooms[room['key']]['play_ids']:
            user_db[user]['last_callback'] = await bot.send_message(
                                text=LEXICON_RU['begin_main_drawing'],
                                chat_id=user,
                                reply_markup=keyboard
                                                                    )
            user_db[user]['room_id'] = room['key']

            await user_db[user]['state'].set_state(FSMInitDrawing.set_victim)
        await callback.answer()
    else:
        await callback.answer(text=LEXICON_RU['stop_recruitment_button_fail'])


@router.callback_query(StateFilter(FSMInitDrawing.set_victim), lambda x: x.data == str(x.from_user.id))
async def pizdezh_command(callback: CallbackQuery):
    await callback.answer(text='Не пизди')


@router.callback_query(StateFilter(FSMInitDrawing.set_victim), F.data == 'wrong')
async def process_prev_victim_wrong(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    room_key = await state.get_data()
    keyboard = inline_keyboard_maker(3, **{str(x[0]): x[1] for x in map(lambda x: (x, user_db[x]['name']), draw_rooms[room_key['key']]['play_ids'])})
    user_db[callback.from_user.id]['last_callback'] = await callback.message.answer(
                                    text=LEXICON_RU['begin_main_drawing'],
                                    reply_markup=keyboard
                                                                                    )
    await callback.answer()


@router.callback_query(StateFilter(FSMInitDrawing.set_victim), F.data == 'right')
async def process_prev_victim_command(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['last_callback'] = callback.message.message_id
    room = await state.get_data()
    # ВНИМАНИЕ, к чему это здесь расписано, я сделал итератор из режимов и текстов к ним
    # За тем, чтоб состояния активировались те, что нужны, чтоб действовали только нужные хендлеры
    # Если например жанров не будет, то состояние выберется исходя из того есть другие режимы или нет
    # Например, если Условия нужно задавать, то в итераторе они появятся, текст будет относиться к условиям и состояние
    # Будет set_conditions. Так мы можем сколько угодно режимов добавлять, вообще нет проблем, если они будут выбраны
    # Инициатором или нет
    # Итератор был заменён на список, в будущем все равно поменяю на итератор

    modes: dict[str, tuple[FSMInitDrawing, dict[str, dict | InlineKeyboardMarkup]]] = \
            {'genres_counts': (FSMInitDrawing.set_prev_genre, {'text': LEXICON_RU['choose_prev_genres'], 'reply_markup': inline_keyboard_maker(3, **LEXICON_GENRES)
                                                               }
                               ),
             'conditions_counts': (FSMInitDrawing.set_new_conditions, {'text': LEXICON_RU['set_conditions']}),
             }
    handlers_modes = [mode for name, mode in modes.items() if draw_rooms[room['key']][name]]
    final_decision = (FSMInitDrawing.the_end, {'text': LEXICON_RU['almost_end'], 'reply_markup': inline_keyboard_maker(1, 'quit')})

    handlers_modes.append(final_decision)
    await state.update_data(needed_states=handlers_modes)
    stating, message_text = handlers_modes[user_db[callback.from_user.id]['modes']['drawing']['step']]
    user_db[callback.from_user.id]['modes']['drawing']['step'] += 1
    await callback.message.delete()
    user_db[callback.from_user.id]['last_callback'] = await callback.message.answer(**message_text)
    await state.set_state(stating)


@router.callback_query(StateFilter(FSMInitDrawing.set_victim),
                       lambda x: x.data.isdigit())
async def process_check_id_process(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['last_callback'] = callback.message.message_id
    await callback.message.delete()
    # Сохраняет человека в список предыдущих людишек, перезапишет, если вдруг человек оказался не тот
    await state.update_data(prev_victim=int(callback.data))
    user_db[callback.from_user.id]['last_callback'] = await callback.message.answer_photo(
            photo=user_db[int(callback.data)]['photo_id'],
            caption=f'Имя: {user_db[int(callback.data)]["name"]}\n'
                    f'Возраст: {user_db[int(callback.data)]["age"]}\n'
                    f'Пол: {user_db[int(callback.data)]["gender"]}\n',
            reply_markup=inline_keyboard_maker(2, 'right', 'wrong')
    )


@router.message(StateFilter(FSMInitDrawing.stop_requit))
async def process_prev_victim_fail(message: Message):
    await message.answer(LEXICON_RU['fail_button'])


@router.callback_query(StateFilter(FSMInitDrawing.set_prev_genre),
                       or_f(F.data == 'thats_all', lambda x: len(user_db[x.from_user.id]['modes']['drawing']['prev_genders']) == 2))
async def process_filled_genres_command(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['last_callback'] = callback.message.message_id
    if callback.data != 'thats_all':
        user_db[callback.from_user.id]['modes']['drawing']['prev_genders'].append(callback.data)
    room_key = await state.get_data()
    stating, message_text = room_key['needed_states'][user_db[callback.from_user.id]['modes']['drawing']['step']]
    user_db[callback.from_user.id]['modes']['drawing']['step'] += 1
    user_db[callback.from_user.id]['last_callback'] = await callback.message.edit_text(**message_text)
    await state.set_state(stating)


@router.callback_query(StateFilter(FSMInitDrawing.set_prev_genre))
async def process_set_genre_command(callback: CallbackQuery):
    user_db[callback.from_user.id]['last_callback'] = callback.message.message_id
    user_db[callback.from_user.id]['modes']['drawing']['prev_genders'].append(callback.data)
    await callback.answer(text=LEXICON_RU['added'])


@router.message(Command(commands='conditions_cancel'), StateFilter(FSMInitDrawing.set_new_conditions))
async def cancel_condey_command(message: Message):

    user_db[message.from_user.id]['modes']['drawing']['set_conditions'] = []
    await message.answer(text=LEXICON_RU['conditions_again'])


@router.message(StateFilter(FSMInitDrawing.set_new_conditions),
                lambda x: len(x.text) <= 300)
async def process_fill_conditions(message: Message, state: FSMContext):
    room = await state.get_data()
    conds = user_db[message.from_user.id]['modes']['drawing']['set_conditions']
    conds.append(message.text)
    draw_rooms[room['key']]['all_conditions'].append(message.text)

    if len(conds) >= draw_rooms[room['key']]['conditions_counts']:
        user_db[message.from_user.id]['last_callback'] = await message.answer(text=LEXICON_RU['check'],
                             reply_markup=inline_keyboard_maker(1, 'agree_button'))
    else:
        await message.answer(text=LEXICON_RU['more'])


@router.callback_query(StateFilter(FSMInitDrawing.set_new_conditions), F.data == 'agree_button')
async def process_accept_conditions_command(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['last_callback'] = callback.message.message_id
    await callback.message.delete()
    room_key = await state.get_data()
    stating, message_text = room_key['needed_states'][user_db[callback.from_user.id]['modes']['drawing']['step']]
    user_db[callback.from_user.id]['modes']['drawing']['step'] += 1
    await callback.message.answer(**message_text)
    await state.set_state(stating)
    await callback.answer()


@router.message(StateFilter(FSMInitDrawing.set_new_conditions))
async def process_fill_cond_fail(message: Message):
    await message.answer(text=LEXICON_RU['too_long'])


@router.message(StateFilter(FSMInitDrawing.the_end))
async def process_end_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['press_the_button'])


@router.callback_query(StateFilter(FSMInitDrawing.the_end), F.data == 'quit')
async def process_quit_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_db[callback.from_user.id]['last_callback'] = callback.message.message_id
    await state.set_state(default_state)
    await callback.message.edit_text(text=callback.message.text)
    room = await state.get_data()
    draw_rooms[room['key']]['over'].add(callback.from_user.id)
    if draw_rooms[room['key']]['over'] == draw_rooms[room['key']]['play_ids']:
        modes = list(filter(lambda mode: draw_rooms[room['key']][mode], ['genres_counts', 'conditions_counts']))  # Потом переделаю в норм функцию, нужны те моды, которые у нас были задействованы
        for user_id in sorted(draw_rooms[room['key']]['play_ids'], key=lambda x: user_db[x]['modes']['drawing']['prev_victim']):
            await bot.send_photo(photo=user_db[user_id]['photo_id'],
                                 caption=f"{generate(draw_rooms[room['key']], user_id, *modes)}\n{LEXICON_RU['the_end']}",  # Здесь результаты будут в будущем
                                 chat_id=user_id)
        for user in draw_rooms[room['key']]['play_ids']:
            user_db[user]['modes']['drawing'] = False
        del draw_rooms[room['key']]
