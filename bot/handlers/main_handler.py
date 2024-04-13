from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from tg_bot.bot.text import GREETING, INFO_COMPACT
from tg_bot.bot.kb import main_kb

router_main = Router()

@router_main.message(Command("start"))
async def start_handler(msg:Message):
    await msg.answer(GREETING)
    await msg.answer('Выберете команду: ', reply_markup=main_kb())
    
@router_main.message(Command("help"))
async def help_handler(msg:Message):
    await msg.answer(INFO_COMPACT, parse_mode='Markdown')
    await msg.answer('Выберете команду: ', reply_markup=main_kb())

@router_main.callback_query(F.data == 'help')
async def help_handler(callback:CallbackQuery):
    await callback.message.answer(INFO_COMPACT, parse_mode='Markdown')
    await callback.message.answer('Выберете команду: ', reply_markup=main_kb())