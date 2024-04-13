import asyncio
from db.db import Database
from utils import get_balance, get_token_price

db = Database()

async def update_balances(bot):
    while True:
        balance = db.get_all_balances()
        print("balance_update")
        for row in balance:
            wallet = db.get_wallet(row[10])

            new_balance = get_balance(wallet[2], row[2], row[8])
            new_balance = new_balance if new_balance else row[3]

            new_price = get_token_price(row[1])
            new_price = new_price if new_price else row[4]

            if (abs(row[3] - new_balance) > 10**(-6) or abs(row[4] - new_price) > 10**(-6)):
                d_balance = row[3] - new_balance

                change = "+" if d_balance > 0 else ""
                if (row[6] and abs(d_balance) > row[7]):
                    await bot.send_message(chat_id=row[9], 
                        text=f"Баланс {row[1]} в {wallet[1]} изменился: *{change}{round(d_balance, 4)}*",
                        parse_mode='Markdown'
                    )
                    
                db.update_last_known_balance(row[0], new_balance, new_price)
        
        await asyncio.sleep(120)   # 900


async def update_wallets(bot):
    while True:
        wallet = db.get_all_wallets()
        print("wallet_update")
        for row in wallet:
            last_sum = row[3]
            new_sum = db.update_last_known_sum(row[0])

            d_sum = last_sum - new_sum
            change = "+" if d_sum > 0 else ""
            if (abs(d_sum) > 10**(-5)):
                await bot.send_message(chat_id=row[4], 
                    text=f"Баланс {wallet[1]} изменился: *{change}{round(d_sum, 4)}*",
                    parse_mode='Markdown'
                )
                        
        await asyncio.sleep(120)