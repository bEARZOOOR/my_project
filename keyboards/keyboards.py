
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


add_auto_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Добавить автомобиль",
    callback_data="add_auto_but_pressed"
)

check_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Список автомобилей",
    callback_data="info_but_pressed"
)

check_lic_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Список авто с линецзией",
    callback_data="info_lic_but_pressed"
)

edite_car: InlineKeyboardButton = InlineKeyboardButton(
    text="Редактировать",
    callback_data="edite_auto_but_pressed"
)

add_lic_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Оформить лицензию",
    callback_data="add_lic_but_pressed"
)


title_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[add_auto_but, add_lic_but],
                     [check_but, edite_car],
                     [check_lic_but]])


