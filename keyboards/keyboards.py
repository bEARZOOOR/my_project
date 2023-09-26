
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)

# Кнопки начального меню
auto_actions: InlineKeyboardButton = InlineKeyboardButton(
    text="Авто",
    callback_data="auto_actions_pressed"
)
license_actions: InlineKeyboardButton = InlineKeyboardButton(
    text="Лицензии",
    callback_data="license_actions_pressed"
)
financial_actions: InlineKeyboardButton = InlineKeyboardButton(
    text="Финансы",
    callback_data="financial_actions_pressed"
)

# Кб начального меню
title_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[auto_actions],
                     [license_actions],
                     [financial_actions]]
)

# Кнопки редактирование авто
add_auto_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Добавить авто",
    callback_data="add_auto_but_pressed"
)

check_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Список авто",
    callback_data="info_but_pressed"
)

edite_car_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Редактировать",
    callback_data="edite_auto_but_pressed"
)

rm_car_but: InlineKeyboardButton = InlineKeyboardButton(
    text= "Удалить авто",
    callback_data="rm_car_but_pressed"
)

# Кб редактирования авто
auto_actions_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[add_auto_but, rm_car_but],
                     [check_but, edite_car_but],])

# Кнопки лицензии
check_lic_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Список авто с лицензией",
    callback_data="info_lic_but_pressed"
)

add_lic_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Оформить лицензию",
    callback_data="add_lic_but_pressed"
)

rm_lic_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Удалить лицензию",
    callback_data="rm_lic_but_pressed"
)

# Кб лиц.
license_actions_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[add_lic_but, check_lic_but],
                     [rm_lic_but]]
)

edite_brand_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Ред. бренд",
    callback_data="edite_brand_but_pressed"
)
edite_model_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Ред. модель",
    callback_data="edite_model_but_pressed"
)
edite_year_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Ред. год",
    callback_data="edite_year_but_pressed"
)
edite_color_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Ред. цвет",
    callback_data="edite_color_but_pressed"
)
edite_license_numb_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Ред. гос.номер",
    callback_data="edite_lic_numb_but_pressed"
)
edite_full_name_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Ред. ФИО",
    callback_data="edite_full_name_but_pressed"
)
edite_phone_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Ред. телефон",
    callback_data="edite_phone_but_pressed"
)
edite_monthly_payment_but: InlineKeyboardButton = InlineKeyboardButton(
    text="Ред. ежем.платеж",
    callback_data="edite_monthly_pay_but_pressed"
)

edite_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[edite_brand_but, edite_model_but],
                     [edite_year_but, edite_color_but],
                     [edite_license_numb_but, edite_full_name_but],
                     [edite_phone_but, edite_monthly_payment_but]]
)