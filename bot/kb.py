import types
from aiogram.utils.keyboard  import InlineKeyboardBuilder
from db.db import Database

db = Database()
def main_kb():    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='Баланс кошельков', callback_data='wallets'))
    builder.add(types.InlineKeyboardButton(text='Посмотреть токены', callback_data='walletmenu'))
    builder.add(types.InlineKeyboardButton(text='Удалить кошелёк', callback_data='deletewallet'))
    builder.add(types.InlineKeyboardButton(text='Добавить кошелёк', callback_data='addwallet'))
    builder.add(types.InlineKeyboardButton(text='Помощь', callback_data='help'))

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def make_wallet_kb(user_id):
    wallets = db.get_user_wallets(user_id)
    builder = InlineKeyboardBuilder()
    for i in wallets:
        builder.add(types.InlineKeyboardButton(text=i[1], callback_data=str(i[0])))

    builder.adjust(3)

    return builder.as_markup(resize_keyboard=True)

def make_token_kb(wallet_id):
    tokens = db.get_wallet_tokens(wallet_id)
    builder = InlineKeyboardBuilder()
    for i in tokens:
        builder.add(types.InlineKeyboardButton(text=i[1], callback_data='token_'+str(i[0])))

    builder.adjust(3)

    return builder.as_markup(resize_keyboard=True)

def make_token_menu(token_id, track):    
    builder = InlineKeyboardBuilder()
    text = 'Не уведомлять об изменениях' if track else 'Уведомлять об изменениях'
    builder.add(types.InlineKeyboardButton(text=text, callback_data='track_'+str(token_id)))
    builder.add(types.InlineKeyboardButton(text='Поменять значение', callback_data='delta_'+str(token_id)))
   

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)