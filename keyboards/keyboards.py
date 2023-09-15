
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


lic_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Создать лицензию",
    callback_data="lic_but_pressed"
)

check_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Список клиентов",
    callback_data="check_but_pressed"
)

keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[lic_but],
                     [check_but]])