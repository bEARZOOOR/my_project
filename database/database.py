import sqlite3


class DatabaseManager:
    db_path = "./database/car.db"
    with sqlite3.connect(db_path) as connect_db:
        cursor = connect_db.cursor()


    async def create_table(self) -> None:

        self.connect_db.execute("""
                    CREATE TABLE IF NOT EXISTS auto(
                    rowid INTEGER PRIMARY KEY,
                    brand TEXT,
                    model TEXT,
                    year TEXT,
                    color TEXT,
                    license_numb TEXT,
                    license INTEGER DEFAULT 0,
                    full_name TEXT,
                    phone TEXT,
                    monthly_payment TEXT,
                    date NULL);
                                """)
            
        self.connect_db.commit()


        self.connect_db.execute("""
                                CREATE TABLE IF NOT EXISTS finance(
                                user_id INTEGER,
                                month_count INTEGER,
                                date_payment INTEGER,
                                reg_payment INTEGER DEFAULT 0
                                );
                                """)
        self.connect_db.commit()


    async def close_connection(self) -> None:

        self.connect_db.close()
'''
db_manager: DatabaseManager = DatabaseManager()

cursor = db_manager.connect_db.cursor()
query = """
    SELECT user_id,
           month_count,
           date_payment,
           reg_payment
           FROM finance WHERE user_id = 1
"""
filter = lambda x: "Да" if x == 1 else "нет"
res = ""
j = cursor.execute(query).fetchall()
for i in j:
    res += f"месяц: {str(i[1])} | дата: {str(i[2])} | оплата: {filter(str(i[3]))}\n"

print(res)
'''