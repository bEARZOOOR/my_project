from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from keyboards.keyboards import title_kb, finance_kb
from aiogram.types import CallbackQuery
from database.database import DatabaseManager
from datetime import datetime



db_manager: DatabaseManager = DatabaseManager()
router: Router = Router()


class FSMShowPayment(StatesGroup):
    fill_id = State()


@router.callback_query((F.data == "show_payment_but_pressed"), StateFilter(default_state))
async def process_check_info_payments_start(callback:CallbackQuery, state: FSMContext):

    await callback.message.answer(text="Введите ID автомобиля: ")
    await state.set_state(FSMShowPayment.fill_id)
    await callback.answer()


@router.message(StateFilter(FSMShowPayment.fill_id))
async def process_check_info_payments_over(message: Message, state: FSMContext):

    await state.update_data(id = message.text)

    values = await state.get_data()
    edite_values = tuple(values.values())
    cursor = db_manager.connect_db.cursor()
    query = """
    SELECT month_count,
           date_payment,
           reg_payment
           FROM finance
           WHERE user_id == {}
    """.format(edite_values[0])
    filter = lambda x: "Да" if x == 1 else "нет"
    edite_result = ""
    data_payments = cursor.execute(query).fetchall()
    for line in data_payments:
        edite_result += f"месяц: {str(line[0])} | дата: {str(line[1])} | оплата: {filter(str(line[2]))}\n"
    await state.clear()
    await message.answer("Просмотр статистики платежей: \n")
    await message.answer(edite_result)
   

@router.callback_query((F.data == "financial_actions_pressed"), StateFilter(default_state))
async def process_check_info(callback:CallbackQuery):
    await callback.message.answer(text='Выберите в меню, '
                                       'что вас интересует:',
                                  reply_markup=finance_kb)
    await callback.answer()
