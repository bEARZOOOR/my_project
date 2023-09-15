from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from keyboards.keyboards import keyboard
from aiogram.types import CallbackQuery
from database.database import DatabaseManager



db_manager: DatabaseManager = DatabaseManager()
router: Router = Router()


class FSMFillForm(StatesGroup):

    fill_full_name = State()
    fill_phone = State() 
    fill_brand = State()
    fill_model = State()
    fill_year = State()
    fill_color = State()
    fill_license_numb = State()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Выберите в меню, '
                              'что вас интересует:',
                              reply_markup=keyboard)



@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего.\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /start и '
                              'выберите "Создать лицензию')


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из заполнения анкеты\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /start и '
                              'выберите "Создать лицензию')

    await state.clear()


@router.callback_query((F.data == "lic_but_pressed"), StateFilter(default_state))
async def process_fsm_full_name_sent(callback:CallbackQuery, state:FSMContext):

    await callback.message.answer(text="Началось заполнение анкеты: \n\n")
    await callback.message.answer(text="Пожалуйста, введите ваше ФИО: ")

    await state.set_state(FSMFillForm.fill_full_name)

    await callback.answer()


@router.message(StateFilter(FSMFillForm.fill_full_name))
async def process_phone_sent(message: Message, state: FSMContext):

    await state.update_data(full_name=message.text)

    await message.answer(text='Введите ваш номер телефона: ')

    await state.set_state(FSMFillForm.fill_phone)



@router.message(StateFilter(FSMFillForm.fill_phone))
async def process_brand_sent(message: Message, state: FSMContext):

    await state.update_data(phone=message.text)

    await message.answer(text='Введите марку: ')

    await state.set_state(FSMFillForm.fill_brand)




@router.message(StateFilter(FSMFillForm.fill_brand))
async def process_model_sent(message: Message, state: FSMContext):

    await state.update_data(brand=message.text)

    await message.answer(text='Введите модель: ')

    await state.set_state(FSMFillForm.fill_model)




@router.message(StateFilter(FSMFillForm.fill_model))
async def process_year_sent(message: Message, state: FSMContext):

    await state.update_data(model=message.text)

    await message.answer(text='Введите год выпуска: ')

    await state.set_state(FSMFillForm.fill_year)



@router.message(StateFilter(FSMFillForm.fill_year))
async def process_color_sent(message: Message, state: FSMContext):

    await state.update_data(year=message.text)

    await message.answer(text='Введите цвет: ')

    await state.set_state(FSMFillForm.fill_color)



@router.message(StateFilter(FSMFillForm.fill_color))
async def process_license_numb_sent(message: Message, state: FSMContext):

    await state.update_data(color=message.text)

    await message.answer(text='Введите гос. номер: ')

    await state.set_state(FSMFillForm.fill_license_numb)


@router.message(StateFilter(FSMFillForm.fill_license_numb))
async def process_fsm_over(message: Message, state: FSMContext):

    await state.update_data(license_numb=message.text)

    query = """
        INSERT INTO license (full_name, phone, brand, model, year, color, license_numb)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    values = await state.get_data()
    edite_values = tuple(values.values())
    db_manager.connect_db.execute(query, edite_values)
    db_manager.connect_db.commit()
    #user_dict[message.from_user.id] = values

    await state.clear()

    await message.answer(text='Спасибо! Ваши данные сохранены!\n\n')
    await message.answer(text='Чтобы посмотреть данные \n'
                                'всех клиентов выберите: \n'
                                '"Список клиентов"',
                                reply_markup=keyboard)



@router.callback_query((F.data == "check_but_pressed"), StateFilter(default_state))
async def process_check_info(callback:CallbackQuery):
    cursor = db_manager.connect_db.cursor()
    query = "SELECT * FROM license"
    await callback.message.answer("Список всех клиентов: \n")
    for i in cursor.execute(query):
        id,full_name,phone,brand,model,year,color,license_numb=i
        await callback.message.answer(
                    f'ID клиента: {id}\n'
                    f'ФИО: {full_name}\n'
                    f'Телефон: {phone}\n'
                    f'Марка: {brand}\n'
                    f'Модель: {model}\n'
                    f'Год выпуска: {year}\n'
                    f'Цвет: {color}\n'
                    f'Гос.номер: {license_numb}\n'
                    )
                
    await callback.answer()