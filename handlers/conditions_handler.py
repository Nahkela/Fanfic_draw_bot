from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Text, CommandStart
from random import sample
from lexicon.lexicon import LEXICON_RU
from Base.Base import states, user_ids, WriteAbility
from keyboards.keyboards import conditions_kb

router = Router()

print('Hi')


@router.message(Text(text=LEXICON_RU['get_conditions_button']), lambda message: states['conditions_count'] != states['names_count'] * 2)
async def get_conditions_process(message: Message):
    await message.answer(text='Твои друганы тугодумы, подожи ещё')


@router.message(Text(text=LEXICON_RU['get_conditions_button']), lambda message: user_ids[message.from_user.id]['got_conditions'])
async def get_conditions_process(message: Message):
    await message.answer(text='\n'.join([f'{num}) {con}' for num, con in enumerate(user_ids[message.from_user.id]['got_conditions'], 1)]))


@router.message(Text(text=LEXICON_RU['get_conditions_button']))
async def get_conditions_process(message: Message):
    personal_conditions = [con for con in states['conditions'] if con not in user_ids[message.from_user.id]['own_conditions']]
    own_conditions = sample(personal_conditions, 2)
    user_ids[message.from_user.id]['got_conditions'] = own_conditions
    for cond in own_conditions:
        states['conditions'].remove(cond)
    await message.answer(text='\n'.join([f'{num}) {con}' for num, con in enumerate(user_ids[message.from_user.id]['got_conditions'], 1)]))


@router.message(CommandStart())
async def late_start_process(message: Message):
    await message.answer(text=LEXICON_RU['late_start'])


@router.message(F.text, WriteAbility(user_ids, states['accepted_count_condition']-1))
async def write_conditions_process(message: Message):
    user_ids[message.from_user.id]['own_conditions'].append(message.text)
    states['conditions'].append(message.text)
    states['conditions_count'] += 1
    print('ХАЙ')
    await message.answer(text='Ешшо условие')


@router.message(F.text, WriteAbility(user_ids, states['accepted_count_condition']))
async def write_conditions_process(message: Message):
    user_ids[message.from_user.id]['own_conditions'].append(message.text)
    states['conditions'].append(message.text)
    states['conditions_count'] += 1
    print('ХААААЙ')
    await message.answer(text=LEXICON_RU['wait_for_conditions'],
                         reply_markup=conditions_kb)

