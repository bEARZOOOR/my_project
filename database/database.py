import sqlite3


class DatabaseManager:
    db_path = "./database/car.db"
    with sqlite3.connect(db_path) as connect_db:
        cursor = connect_db.cursor()


    async def create_table(self) -> None:

        self.connect_db.execute("""
                    CREATE TABLE IF NOT EXISTS auto(
                    id INTEGER PRIMARY KEY,
                    brand TEXT,
                    model TEXT,
                    year TEXT,
                    color TEXT,
                    license_numb TEXT,
                    license INTEGER DEFAULT 0,
                    full_name TEXT,
                    phone TEXT,
                    monthly_payment TEXT);
                                """)
            
        self.connect_db.commit()


    async def close_connection(self) -> None:

        self.connect_db.close()
'''
db_manager: DatabaseManager = DatabaseManager()

cursor = db_manager.cursor
query = "SELECT rowid FROM license"

cursor.execute(query)
print(cursor.fetchall())
'''