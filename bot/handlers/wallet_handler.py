from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from tg_bot.bot.states import Wallet, DeleteWallet, WalletWatch, TokenWatch
from tg_bot.bot.utils import is_wallet_connected, createAsset
from tg_bot.bot.text import NO_WALLET, CHOOSE, ADD_WALLET_MESSAGE, WALLET_DOESNT_EXIST, WALLET_LIST
from tg_bot.bot.kb import make_wallet_kb, make_token_kb, make_token_menu
from tg_bot.bot.db.db import Database
from aiogram.filters import Command, StateFilter
router_wallet = Router()
db = Database()

@router_wallet.message(Command('wallets'))
async def wallets_handler(msg:Message):
    user = msg.from_user.id
    wallets = db.get_user_wallets(user)
    if len(wallets) == 0:
        await msg.answer(NO_WALLET)
    else:
        answer = WALLET_LIST
        for i in wallets:
            answer += f"Wallet: {i[1]} \n\
Balance:{i[3]} \n\n"
            
        await msg.answer(text=answer, parse_mode='Markdown')


@router_wallet.callback_query(F.data == 'wallets')
async def wallets_handler(callback:CallbackQuery):
    user = callback.from_user.id
    wallets = db.get_user_wallets(user)
    if len(wallets) == 0:
        await callback.message.answer(NO_WALLET)
    else:
        answer = WALLET_LIST
        for i in wallets:
            answer += f"Wallet: {i[1]} \n\
Balance:{i[3]} \n\n"
            
        await callback.message.answer(text=answer, parse_mode='Markdown')

@router_wallet.message(Command('addwallet'))
async def add_wallet(msg:Message, state:FSMContext):
    await msg.answer('Введите адресс кошелька, который хотите добавить:')
    await state.set_state(Wallet.wallet_address)

@router_wallet.message(Wallet.wallet_address, F.text)
async def add_wallet_address(msg:Message, state:FSMContext):
    await state.update_data(wallet_address = msg.text) 
    await msg.answer(text='Теперь, задайте название для нового кошелька: ')
    await state.set_state(Wallet.wallet_name)

@router_wallet.message(Wallet.wallet_name, F.text)
async def add_wallet_name(msg:Message, state:FSMContext):
    user_data = await state.get_data()
    user_id = msg.from_user.id
    wallet_address = user_data['wallet_address']
    wallet_name = msg.text

    if not is_wallet_connected(wallet_address):
        await msg.answer(WALLET_DOESNT_EXIST)
        await msg.answer('Введите другой адресс:')
        await state.clear()
        await state.set_state(Wallet.wallet_address)
        return
    if not db.check_wallet(wallet_address, user_id):
        await msg.answer('Такой кошелёк уже был добавлен')
        await state.clear()
        return
    wallet_id = db.add_wallet(user_id, wallet_name, wallet_address)
    await msg.answer(text=f"Вы добавили кошелёк с названием {wallet_name} и адресом {wallet_address}.")
    createAsset(wallet_address, wallet_id, user_id)
    await state.clear()
    

@router_wallet.callback_query(F.data == 'deletewallet')
async def delete_wallet_handler(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer('Выберете кошелёк:', reply_markup=make_wallet_kb(), parse_mode='Markdown')
    await state.set_state(DeleteWallet.wallet_id)

@router_wallet.callback_query(DeleteWallet.wallet_id, F.text)
async def delete_wallet(callback:CallbackQuery, state:FSMContext):
    user_id = callback.from_user.id
    await db.delete_wallet(user_id,callback.data)
    await callback.message.answer(f"Вы удалили кошелёк!")
    await state.clear()