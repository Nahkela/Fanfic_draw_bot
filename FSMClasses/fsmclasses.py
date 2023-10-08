from aiogram.fsm.state import StatesGroup, State


class FSMFillform(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    upload_photo = State()
    fill_fanfics_writer = State()
