from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.inline.callback_data import admin_callback
from keyboards.inline.choice_button import admin_panel
from loader import dp, bot
from utils.db.models import Database, Users, session

db = Database()
list_of_usrers = db.get_unconfirmed_users()


@dp.message_handler(Command('confirm_user'))
async def confirm_user(message: types.Message):
    if message.chat.id not in ADMINS:
        await message.answer('You cannot use this command because you are not an admin...')
    else:
        users = []
        try:
            for user in list_of_usrers:
                users.append(user.user_id)

            text = f'Confirm Users {users[0]}'
            await message.answer(text, reply_markup=admin_panel)
        except IndexError:
            await message.answer('No more unconfirmed users')


@dp.callback_query_handler(admin_callback.filter(bool='confirm_user'))
async def confirm_user(call: CallbackQuery):
    data = []
    for user in list_of_usrers:
        data.append({
            'id': user.id,
            'user_id': user.user_id,
            'confirmed': user.confirmed
        })
    if len(data) >= 1:
        db.confirm_user(data[0]['user_id'], True)

        await bot.edit_message_text(text=f'You have successfully confirmed user: {data[0]["id"]}',
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)

    else:
        await call.message.answer('No more unconfirmed users 2')


