from aiogram.fsm.state import State, StatesGroup

class Wallet(StatesGroup):
    wallet_name = State()
    wallet_address = State()
    
class DeleteWallet(StatesGroup):
    wallet_id = State()

class WalletWatch(StatesGroup):
    wallet_id = State()

class TokenWatch(StatesGroup):
    delta = State()

class UserState(StatesGroup):
    State = State()