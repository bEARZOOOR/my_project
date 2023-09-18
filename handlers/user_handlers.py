from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from keyboards.keyboards import title_kb
from aiogram.types import CallbackQuery
from database.database import DatabaseManager



db_manager: DatabaseManager = DatabaseManager()
router: Router = Router()


class FSMAutoAdd(StatesGroup):

    fill_brand = State()
    fill_model = State()
    fill_year = State()
    fill_color = State()
    fill_license_numb = State()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Выберите в меню, '
                              'что вас интересует:',
                              reply_markup=title_kb)



@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего.\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /start и '
                              'выберите "Добавить автомобиль')


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из заполнения анкеты\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /start и '
                              'выберите "Добавить автомобиль')

    await state.clear()


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
    query = """SELECT
                    id,
                    brand,
                    model,
                    year,
                    color,
                    license_numb,
                    license
                    FROM auto"""
    license_filter = lambda x: "Да" if x == 1 else "Нет"
    await callback.message.answer("Список автомобилей: \n")
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


@router.callback_query((F.data == "info_lic_but_pressed"), StateFilter(default_state))
async def process_check_info_lic(callback:CallbackQuery):
    cursor = db_manager.connect_db.cursor()
    query = """SELECT
                    id,
                    brand,
                    model,
                    year,
                    color,
                    license_numb,
                    license
                    FROM auto WHERE license == 1"""
    license_filter = lambda x: "Да" if x == 1 else "Нет"
    await callback.message.answer("Список автомобилей с лицензией: \n")
    for values in cursor.execute(query):
        id,brand,model,year,color,license_numb, license = values
        await callback.message.answer(
                    f'ID клиента: {id}\n'
                    f'Марка: {brand}\n'
                    f'Модель: {model}\n'
                    f'Год выпуска: {year}\n'
                    f'Цвет: {color}\n'
                    f'Гос.номер: {license_numb}\n'
                    f'Лицензия: {license_filter(int(license))}\n'
                    )
                
    await callback.answer()

###########################################################

class FSMLicenseAdd(StatesGroup):
    fill_id = State()
    fill_full_name = State()
    fill_phone = State()
    fill_monthly_payment = State()



@router.callback_query((F.data == "add_lic_but_pressed"), StateFilter(default_state))
async def process_fsm_id_sent(callback:CallbackQuery, state:FSMContext):

    await callback.message.answer(text="Началось оформление лицензии: \n\n")
    await callback.message.answer(text="Введите выбранный ID: ")

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
    query = """
    UPDATE auto SET full_name = '{}',
                    phone = '{}',
                    monthly_payment = '{}',
                    license = '1'
                    WHERE id == '{}'
    """.format(edite_values[1], edite_values[2], edite_values[3], edite_values[0])

    db_manager.connect_db.execute(query)
    db_manager.connect_db.commit()

    await state.clear()

    await message.answer(text='Спасибо! Ваши данные сохранены!\n\n',
                         reply_markup=title_kb)