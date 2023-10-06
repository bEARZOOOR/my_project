from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from keyboards.keyboards import title_kb, auto_actions_kb,  edite_kb
from aiogram.types import CallbackQuery
from database.database import DatabaseManager
from datetime import datetime


db_manager: DatabaseManager = DatabaseManager()
router: Router = Router()


class FSMAutoAdd(StatesGroup):

    fill_brand = State()
    fill_model = State()
    fill_year = State()
    fill_color = State()
    fill_license_numb = State()


@router.callback_query((F.data == "add_auto_but_pressed"), StateFilter(default_state))
async def process_fsm_brand_sent(callback:CallbackQuery, state:FSMContext):

    await callback.message.answer(text="Началось заполнение анкеты: \n\n")
    await callback.message.answer(text="Введите марку: ")

    await state.set_state(FSMAutoAdd.fill_brand)

    await callback.answer()


@router.message(StateFilter(FSMAutoAdd.fill_brand))
async def process_model_sent(message: Message, state: FSMContext):

    await state.update_data(brand=message.text)

    await message.answer(text='Введите модель: ')

    await state.set_state(FSMAutoAdd.fill_model)




@router.message(StateFilter(FSMAutoAdd.fill_model))
async def process_year_sent(message: Message, state: FSMContext):

    await state.update_data(model=message.text)

    await message.answer(text='Введите год выпуска: ')

    await state.set_state(FSMAutoAdd.fill_year)



@router.message(StateFilter(FSMAutoAdd.fill_year))
async def process_color_sent(message: Message, state: FSMContext):

    await state.update_data(year=message.text)

    await message.answer(text='Введите цвет: ')

    await state.set_state(FSMAutoAdd.fill_color)



@router.message(StateFilter(FSMAutoAdd.fill_color))
async def process_license_numb_sent(message: Message, state: FSMContext):

    await state.update_data(color=message.text)

    await message.answer(text='Введите гос. номер: ')

    await state.set_state(FSMAutoAdd.fill_license_numb)


@router.message(StateFilter(FSMAutoAdd.fill_license_numb))
async def process_fsm_over(message: Message, state: FSMContext):

    await state.update_data(license_numb=message.text)

    query = """
        INSERT INTO auto (
            brand,
            model,
            year,
            color,
            license_numb)
        VALUES (?, ?, ?, ?, ?);
    """
    values = await state.get_data()
    edite_values = tuple(values.values())
    db_manager.connect_db.execute(query, edite_values)
    db_manager.connect_db.commit()


    await state.clear()

    await message.answer(text='Спасибо! Ваши данные сохранены!\n\n',
                         reply_markup=title_kb)


@router.callback_query((F.data == "info_but_pressed"), StateFilter(default_state))
async def process_check_info(callback:CallbackQuery):
    cursor = db_manager.connect_db.cursor()
    query = """SELECT rowid,
                      brand,
                      model,
                      year,
                      color,
                      license_numb,
                      license
                      FROM auto"""
    license_filter = lambda x: "Да" if x == 1 else "Нет"
    await callback.message.answer("Список авто: \n")
    for values in cursor.execute(query):
        id,brand,model,year,color,license_numb, license = values
        await callback.message.answer(
                    f'ID клиента: {id}\n'
                    f'Марка: {brand}\n'
                    f'Модель: {model}\n'
                    f'Год выпуска: {year}\n'
                    f'Цвет: {color}\n'
                    f'Гос.номер: {license_numb}\n'
                    f'Лицензия: {license_filter(int(license))}\n',
                    )
                
    await callback.answer()



class FSMCarRm(StatesGroup):
    fill_id = State()

@router.callback_query(F.data == "rm_car_but_pressed", StateFilter(default_state))
async def process_fsm_id2_send(callback:CallbackQuery, state: FSMContext):

    await callback.message.answer(text="Введите ID авто для удаления")

    await state.set_state(FSMCarRm.fill_id)

    await callback.answer()


@router.message(StateFilter(FSMCarRm.fill_id))
async def process_fsm_rm_car_over(message: Message, state: FSMContext):

    await state.update_data(id = message.text)

    values = await state.get_data()
    edite_values = tuple(values.values())
    now = datetime. now()
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

    await message.answer(text='Авто с ID: {} удален!\n\n'.format(edite_values[0]))


# Выбор действий с авто
@router.callback_query((F.data == "auto_actions_pressed"), StateFilter(default_state))
async def process_check_info(callback:CallbackQuery):
    await callback.message.answer(text='Выберите в меню, '
                                       'что вас интересует:',
                                  reply_markup=auto_actions_kb)
    await callback.answer()


@router.callback_query((F.data == "edite_auto_but_pressed"), StateFilter(default_state))
async def process_check_info(callback:CallbackQuery):
    await callback.message.answer(text='Выберите в меню, '
                                       'что вас интересует:',
                                  reply_markup=edite_kb)
    await callback.answer()

# 1
class FSMEditeBrand(StatesGroup):
    fill_id = State()
    fill_brand = State()


@router.callback_query((F.data == "edite_brand_but_pressed"), StateFilter(default_state))
async def process_edite_brand_start(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ID авто\n"
                                       "для внесения изменения: ")
    await state.set_state(FSMEditeBrand.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMEditeBrand.fill_id))
async def process_edite_brand(mesaage: Message, state: FSMContext):

    await state.update_data(id=mesaage.text)
    await mesaage.answer("Введите новые данные: ")
    await state.set_state(FSMEditeBrand.fill_brand)


@router.message(StateFilter(FSMEditeBrand.fill_brand))
async def process_edite_brand_over(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    values = await state.get_data()
    edite_values = tuple(values.values())
    query = """
    UPDATE auto SET brand = "{}"
    WHERE rowid == "{}"
    """.format(edite_values[1], edite_values[0])
    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()
    await state.clear()
    await message.answer(text="Изменения сохранены!\n"
                              "Марка авто была\n"
                              f"изменена на {edite_values[1]}")


# 2
class FSMEditeModel(StatesGroup):
    fill_id = State()
    fill_model = State()


@router.callback_query((F.data == "edite_model_but_pressed"), StateFilter(default_state))
async def process_edite_model_start(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ID авто\n"
                                       "для внесения изменения: ")
    await state.set_state(FSMEditeModel.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMEditeModel.fill_id))
async def process_edite_model(mesaage: Message, state: FSMContext):

    await state.update_data(id=mesaage.text)
    await mesaage.answer("Введите новые данные: ")
    await state.set_state(FSMEditeModel.fill_model)


@router.message(StateFilter(FSMEditeModel.fill_model))
async def process_edite_model_over(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    values = await state.get_data()
    edite_values = tuple(values.values())
    query = """
    UPDATE auto SET model = "{}"
    WHERE rowid == "{}"
    """.format(edite_values[1], edite_values[0])
    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()
    await state.clear()
    await message.answer(text="Изменения сохранены!\n"
                              "Модель авто была\n"
                              f"изменена на {edite_values[1]}")
    

# 3
class FSMEditeYear(StatesGroup):
    fill_id = State()
    fill_year = State()


@router.callback_query((F.data == "edite_year_but_pressed"), StateFilter(default_state))
async def process_edite_year_start(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ID авто\n"
                                       "для внесения изменения: ")
    await state.set_state(FSMEditeYear.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMEditeYear.fill_id))
async def process_edite_year(mesaage: Message, state: FSMContext):

    await state.update_data(id=mesaage.text)
    await mesaage.answer("Введите новые данные: ")
    await state.set_state(FSMEditeYear.fill_year)


@router.message(StateFilter(FSMEditeYear.fill_year))
async def process_edite_year_over(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    values = await state.get_data()
    edite_values = tuple(values.values())
    query = """
    UPDATE auto SET year = "{}"
    WHERE rowid == "{}"
    """.format(edite_values[1], edite_values[0])
    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()
    await state.clear()
    await message.answer(text="Изменения сохранены!\n"
                              "Год авто был\n"
                              f"изменен на {edite_values[1]}")


# 4
class FSMEditeColor(StatesGroup):
    fill_id = State()
    fill_color = State()


@router.callback_query((F.data == "edite_color_but_pressed"), StateFilter(default_state))
async def process_edite_color_start(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ID авто\n"
                                       "для внесения изменения: ")
    await state.set_state(FSMEditeColor.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMEditeColor.fill_id))
async def process_edite_color(mesaage: Message, state: FSMContext):

    await state.update_data(id=mesaage.text)
    await mesaage.answer("Введите новые данные: ")
    await state.set_state(FSMEditeColor.fill_color)


@router.message(StateFilter(FSMEditeColor.fill_color))
async def process_edite_color_over(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    values = await state.get_data()
    edite_values = tuple(values.values())
    query = """
    UPDATE auto SET color = "{}"
    WHERE rowid == "{}"
    """.format(edite_values[1], edite_values[0])
    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()
    await state.clear()
    await message.answer(text="Изменения сохранены!\n"
                              "Цвет авто был\n"
                              f"изменен на {edite_values[1]}")
    

# 5
class FSMEditeLicenseNumb(StatesGroup):
    fill_id = State()
    fill_license_numb = State()


@router.callback_query((F.data == "edite_license_numb_but_pressed"), StateFilter(default_state))
async def process_edite_license_numb_start(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ID авто\n"
                                       "для внесения изменения: ")
    await state.set_state(FSMEditeLicenseNumb.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMEditeLicenseNumb.fill_id))
async def process_edite_license_numb(mesaage: Message, state: FSMContext):

    await state.update_data(id=mesaage.text)
    await mesaage.answer("Введите новые данные: ")
    await state.set_state(FSMEditeLicenseNumb.fill_license_numb)


@router.message(StateFilter(FSMEditeLicenseNumb.fill_license_numb))
async def process_edite_license_numb_over(message: Message, state: FSMContext):
    await state.update_data(license_numb=message.text)
    values = await state.get_data()
    edite_values = tuple(values.values())
    query = """
    UPDATE auto SET license_numb = "{}"
    WHERE rowid == "{}"
    """.format(edite_values[1], edite_values[0])
    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()
    await state.clear()
    await message.answer(text="Изменения сохранены!\n"
                              "Гос.номер авто был\n"
                              f"изменен на {edite_values[1]}")
    

# 6
class FSMEditeFullName(StatesGroup):
    fill_id = State()
    fill_full_name = State()


@router.callback_query((F.data == "edite_full_name_but_pressed"), StateFilter(default_state))
async def process_edite_full_name_start(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ID авто\n"
                                       "для внесения изменения: ")
    await state.set_state(FSMEditeFullName.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMEditeFullName.fill_id))
async def process_edite_full_name(mesaage: Message, state: FSMContext):

    await state.update_data(id=mesaage.text)
    await mesaage.answer("Введите новые данные: ")
    await state.set_state(FSMEditeFullName.fill_full_name)


@router.message(StateFilter(FSMEditeFullName.fill_full_name))
async def process_edite_full_name_over(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    values = await state.get_data()
    edite_values = tuple(values.values())
    query = """
    UPDATE auto SET full_name = "{}"
    WHERE rowid == "{}"
    """.format(edite_values[1], edite_values[0])
    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()
    await state.clear()
    await message.answer(text="Изменения сохранены!\n"
                              "ФИО клиента было\n"
                              f"изменено на {edite_values[1]}")
    

# 7
class FSMEditePhone(StatesGroup):
    fill_id = State()
    fill_phone = State()


@router.callback_query((F.data == "edite_phone_but_pressed"), StateFilter(default_state))
async def process_edite_phone_start(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ID авто\n"
                                       "для внесения изменения: ")
    await state.set_state(FSMEditePhone.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMEditePhone.fill_id))
async def process_edite_phone(mesaage: Message, state: FSMContext):

    await state.update_data(id=mesaage.text)
    await mesaage.answer("Введите новые данные: ")
    await state.set_state(FSMEditePhone.fill_phone)


@router.message(StateFilter(FSMEditePhone.fill_phone))
async def process_edite_phone_over(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    values = await state.get_data()
    edite_values = tuple(values.values())
    query = """
    UPDATE auto SET phone = "{}"
    WHERE rowid == "{}"
    """.format(edite_values[1], edite_values[0])
    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()
    await state.clear()
    await message.answer(text="Изменения сохранены!\n"
                              "телефон клиента был\n"
                              f"изменен на {edite_values[1]}")
    

#
class FSMEditeMonthlyPayment(StatesGroup):
    fill_id = State()
    fill_monthly_payment = State()


@router.callback_query((F.data == "edite_monthly_payment_but_pressed"), StateFilter(default_state)) #
async def process_edite_monthly_payment_start(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ID авто\n"
                                       "для внесения изменения: ")
    await state.set_state(FSMEditeMonthlyPayment.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMEditeMonthlyPayment.fill_id))
async def process_edite_monthly_payment(mesaage: Message, state: FSMContext):

    await state.update_data(id=mesaage.text)
    await mesaage.answer("Введите новые данные: ")
    await state.set_state(FSMEditeMonthlyPayment.fill_monthly_payment)


@router.message(StateFilter(FSMEditeMonthlyPayment.fill_monthly_payment))
async def process_edite_monthly_payment_over(message: Message, state: FSMContext):
    await state.update_data(monthly_payment=message.text)
    values = await state.get_data()
    edite_values = tuple(values.values())
    query = """
    UPDATE auto SET monthly_payment = "{}"
    WHERE rowid == "{}"
    """.format(edite_values[1], edite_values[0])
    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()
    await state.clear()
    await message.answer(text="Изменения сохранены!\n"
                              "Ежем.платеж был\n"
                              f"изменен на {edite_values[1]}")