import psycopg2
DATABASE_URL='postgresql://postgres:pft,fkb19RU@localhost/tg_bot'
class Database:
    def __init__(self, database_url=DATABASE_URL):
        self.conn = psycopg2.connect(database_url)
        self.cursor = self.conn.cursor()

    def add_balance(self, asset,address,balance,price,user_id,network_id,wallet_id):   
        value = balance * price
        self.cursor.execute(f"INSERT INTO tokens (\
                            asset,\
                            address,\
                            balance,\
                            price,\
                            value,\
                            track,\
                            delta,\
                            network_id,\
                            user_id,\
                            wallet_id,\
        ) VALUES ('{asset}', '{address}',{balance}, {price}, {value}, {True}, {0.01}, {network_id}, {user_id}, {wallet_id})")
        self.conn.commit()

    def add_wallet(self, user_id, wallet_name, wallet_address):   
        self.cursor.execute(f"INSERT INTO wallets (\
                            user_id,\
                            name,\
                            address,\
                            sum,\
        ) VALUES ({user_id}, '{wallet_name}','{wallet_address}', {0}) RETURNING id")
        wallet_id = self.cursor.fetchone()[0]       
        self.conn.commit()
        return wallet_id
    
    def check_wallet(self, wallet_address, user_id):
        self.cursor.execute(f"SELECT * FROM wallets WHERE adress = '{wallet_address}' AND user_id = {user_id}")
        if len(self.cursor.fetchall()) == 0:
            return True
        else: return False

    def get_networks(self):
        self.cursor.execute("SELECT * FROM networks")
        return self.cursor.fetchall()
    
    def get_network(self, network_id):
        self.cursor.execute(f"SELECT * FROM networks WHERE id = {network_id}")
        return self.cursor.fetchall()[0]

    def get_user_wallets(self, user):
        self.cursor.execute(f"SELECT * FROM wallets WHERE user_id = {user}")
        return self.cursor.fetchall()
    
    def get_wallet(self, id):
        self.cursor.execute(f"SELECT * FROM wallets WHERE id = {id}")
        return self.cursor.fetchall()[0]
    
    def get_all_balances(self):
        self.cursor.execute(f"SELECT * FROM tokens")
        return self.cursor.fetchall()
    
    def get_all_wallets(self):
        self.cursor.execute(f"SELECT * FROM wallets")
        return self.cursor.fetchall()

    def get_wallet_balances(self, wallet_id):
        self.cursor.execute(f"SELECT * FROM tokens WHERE wallet_id = {wallet_id}")
        return self.cursor.fetchall()
    
    def get_balance(self, id):
        self.cursor.execute(f"SELECT * FROM tokens WHERE id = {id}")
        return self.cursor.fetchall()[0]
    
    def get_sum_wallet(self, wallet_id):
        self.cursor.execute(f"SELECT sum FROM wallets WHERE  id = {wallet_id}")
    
    def update_last_known_sum(self, wallet_id):
        self.cursor.execute(f"SELECT sum(value) as sum_wallet FROM tokens WHERE wallet_id = {wallet_id} ")
        new_sum = self.cursor.fetchone()
        self.cursor.execute(f"UPDATE wallets SET sum = {new_sum[0]} WHERE id = {wallet_id}")
        self.conn.commit()

        return new_sum[0]

    def update_last_known_balance(self, token_id, new_balance, new_price):
        value = new_balance * new_price
        self.cursor.execute(f"UPDATE tokens SET balance = {new_balance}, price = {new_price}, value = {value} WHERE id = {token_id}")
        self.conn.commit()
        self.cursor.execute(f"SELECT * FROM tokens WHERE id = {token_id}")
        return self.cursor.fetchone()

    def update_track_balance(self, token_id, track):
        self.cursor.execute(f"UPDATE tokens SET track = {track} WHERE id = {token_id}")
        self.conn.commit()

    def update_delta_balance(self, token_id, delta):
        self.cursor.execute(f"UPDATE tokens SET delta = {delta} WHERE id = {token_id}")
        self.conn.commit()

    def delete_wallet(self, user_id, wallet_id):
        self.cursor.execute(f"DELETE FROM wallets WHERE id = {wallet_id} AND user_id = {user_id}")
        self.cursor.execute(f"DELETE FROM tokens WHERE wallet_id = {wallet_id} AND user_id = {user_id}")
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()