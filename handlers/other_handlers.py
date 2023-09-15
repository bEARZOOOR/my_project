from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from lexicon.lexicon import LEXICON


router: Router = Router()

# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON["send_echo"])
