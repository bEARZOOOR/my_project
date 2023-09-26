from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from keyboards.keyboards import title_kb, license_actions_kb
from aiogram.types import CallbackQuery
from database.database import DatabaseManager
from datetime import datetime


db_manager: DatabaseManager = DatabaseManager()
router: Router = Router()


@router.callback_query((F.data == "info_lic_but_pressed"), StateFilter(default_state))
async def process_check_info_lic(callback:CallbackQuery):
    cursor = db_manager.connect_db.cursor()
    query = """SELECT rowid,
                      brand,
                      model,
                      year,
                      color,
                      license_numb,
                      license,
                      date,
                      full_name,
                      phone,
                      monthly_payment
                      FROM auto
                      WHERE license == 1"""
    license_filter = lambda x: "Да" if x == 1 else "Нет"
    await callback.message.answer("Список авто с лицензией: \n")
    for values in cursor.execute(query):
        id,brand,model,year,color,license_numb, license, date, full_name, phone, monthly_payment = values
        await callback.message.answer(
                    f'ID клиента: {id}\n'
                    f'Марка: {brand}\n'
                    f'Модель: {model}\n'
                    f'Год выпуска: {year}\n'
                    f'Цвет: {color}\n'
                    f'Гос.номер: {license_numb}\n'
                    f'Лицензия: {license_filter(int(license))}\n'
                    f'Время оформления: {date}\n'
                    "Данные по клиенту: \n"
                    f'ФИО: {full_name}\n'
                    f'Телефон: {phone}\n'
                    f'Ежем.платеж: {monthly_payment}\n'
                    )
                
    await callback.answer()



class FSMLicenseAdd(StatesGroup):
    fill_id = State()
    fill_full_name = State()
    fill_phone = State()
    fill_monthly_payment = State()



@router.callback_query((F.data == "add_lic_but_pressed"), StateFilter(default_state))
async def process_fsm_id_sent(callback:CallbackQuery, state:FSMContext):

    await callback.message.answer(text="Началось оформление лицензии: \n\n")
    await callback.message.answer(text="Введите ID авто для\n"
                                       "оформления лицензии: \n")

    await state.set_state(FSMLicenseAdd.fill_id)

    await callback.answer()


@router.message(StateFilter(FSMLicenseAdd.fill_id))
async def process_full_name_sent(message: Message, state: FSMContext):

    await state.update_data(id = message.text)

    await message.answer(text="Введита ваше ФИО: ")

    await state.set_state(FSMLicenseAdd.fill_full_name)


@router.message(StateFilter(FSMLicenseAdd.fill_full_name))
async def process_phone_sent(message: Message, state: FSMContext):

    await state.update_data(full_name = message.text)

    await message.answer(text="Введите номер телефона: ")

    await state.set_state(FSMLicenseAdd.fill_phone)


@router.message(StateFilter(FSMLicenseAdd.fill_phone))
async def process_monthly_payment_sent(message: Message, state: FSMContext):

    await state.update_data(phone = message.text)

    await message.answer(text="Введите ежемесячный платеж: ")

    await state.set_state(FSMLicenseAdd.fill_monthly_payment)


@router.message(StateFilter(FSMLicenseAdd.fill_monthly_payment))
async def process_fsm_license_over(message: Message, state: FSMContext):

    await state.update_data(monthly_payment = message.text)


    values = await state.get_data()
    edite_values = tuple(values.values())
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    query = """
    UPDATE auto SET full_name = '{}',
                    phone = '{}',
                    monthly_payment = '{}',
                    license = '1',
                    date = '{}'
                    WHERE rowid == '{}'
    """.format(edite_values[1], edite_values[2], edite_values[3], dt_string, edite_values[0])

    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()

    await state.clear()

    await message.answer(text='Лицензия оформлена\n'
                              'Спасибо! Ваши данные сохранены!\n\n',
                         reply_markup=title_kb)
    

# Удаление лицензии
class FSMLicenseRm(StatesGroup):
    fill_id = State()

@router.callback_query(F.data == "rm_lic_but_pressed", StateFilter(default_state))
async def process_fsm_id3_send(callback:CallbackQuery, state: FSMContext):

    await callback.message.answer(text="Введите ID авто для удаления")

    await state.set_state(FSMLicenseRm.fill_id)

    await callback.answer()


@router.message(StateFilter(FSMLicenseRm.fill_id))
async def process_fsm_rm_license_over(message: Message, state: FSMContext):

    await state.update_data(id = message.text)

    values = await state.get_data()
    edite_values = tuple(values.values())
    now = datetime. now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    query = """
    UPDATE auto SET monthly_payment = NULL,
                    license = '0',
                    date = '{}'
                    WHERE rowid == '{}'
    """.format(dt_string, edite_values[0])

    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()


    await state.clear()

    await message.answer(text='лицензия авто с ID: {} удалена {}!\n\n'.format(edite_values[0], dt_string))



#
@router.callback_query((F.data == "license_actions_pressed"), StateFilter(default_state))
async def process_check_info(callback:CallbackQuery):
    await callback.message.answer(text='Выберите в меню, '
                                       'что вас интересует:',
                                  reply_markup=license_actions_kb)
    await callback.answer()
