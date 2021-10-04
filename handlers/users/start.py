from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import CallbackQuery

from data.dialog import WELCOME, HELP
from keyboards.inline.callback_data import callback
from keyboards.inline.choice_button import choice
from loader import dp, bot
from utils.db.models import Database

db = Database()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Hey, {message.from_user.full_name}! What’s up?')
    await message.answer(text=WELCOME)
    await message.answer(text='To book a queue click on the button ', reply_markup=choice)


@dp.callback_query_handler(callback.filter(item_name='staytoqueue'))
async def process_callback_staytoqueue(call: CallbackQuery):
    user_id = call.message.chat.id
    await call.answer(cache_time=1)
    try:
        check_user = db.check_user_exist(user_id)
        position = db.get_current_positon(user_id)
        if check_user:
            await bot.edit_message_text(message_id=call.message.message_id,
                                        chat_id=call.message.chat.id,
                                        text=f'You exist in our base, {position}')
        else:
            db.add_to_queue(user_id)
            await bot.edit_message_text(message_id=call.message.message_id,
                                        chat_id=user_id,
                                        text=f'You have booked successfully!')
    except AttributeError:
        print('ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRR')


@dp.message_handler(Command('position'))
async def get_user_position(message: types.Message):
    result = db.get_current_positon(message.chat.id)
    await message.answer(text=result, parse_mode='Markdown')


@dp.message_handler(Command('help'))
async def support(message: types.Message):
    await message.answer(text=HELP)


