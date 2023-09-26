from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from keyboards.keyboards import title_kb


router: Router = Router()


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
                              'выберите "Добавить авто')


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из заполнения анкеты\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /start и '
                              'выберите "Добавить авто')

    await state.clear()