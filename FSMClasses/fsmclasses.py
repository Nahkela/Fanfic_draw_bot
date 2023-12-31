from aiogram.fsm.state import StatesGroup, State


class FSMFillform(StatesGroup):
    register_begin = State()
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    upload_photo = State()
    fill_fanfics_writer = State()


class FSMInitDrawing(StatesGroup):
    draw_started = State()
    fill_guest_key = State()
    fill_genres_count = State()
    fill_conditions_count = State()
    wait = State()
    set_victim = State()
    invite_guests = State()
    stop_requit = State()
    set_prev_genre = State()
    set_new_conditions = State()
    the_end = State()

