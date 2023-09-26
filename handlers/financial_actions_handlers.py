from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from keyboards.keyboards import title_kb
from aiogram.types import CallbackQuery
from database.database import DatabaseManager
from datetime import datetime



db_manager: DatabaseManager = DatabaseManager()
router: Router = Router()


@router.callback_query((F.data == "financial_actions_pressed"), StateFilter(default_state))
async def process_check_info(callback:CallbackQuery):

    await callback.answer()