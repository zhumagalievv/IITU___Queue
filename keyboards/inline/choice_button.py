from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import callback, admin_callback

choice = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton('Cancel', callback_data=callback.new(item_name='gotoback')),
        InlineKeyboardButton('Reservation', callback_data=callback.new(item_name='staytoqueue'))

    ],
])

admin_panel = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton('Additional Button', callback_data=admin_callback.new(bool='additional')),
        InlineKeyboardButton('Confirm User', callback_data=admin_callback.new(bool='confirm_user'))
    ],
])
