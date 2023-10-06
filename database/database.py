import sqlite3


class DatabaseManager:
    def __init__(self):
        db_path = "./database/car.db"
        self.connect_db = sqlite3.connect(db_path)
        self.cursor = self.connect_db.cursor()


    def create_table(self):

        with self.connect_db:
            self.cursor.execute("""
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


        with self.connect_db:
            self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS finance(
                                user_id INTEGER,
                                month_count INTEGER,
                                date_payment INTEGER,
                                reg_payment INTEGER DEFAULT 0
                                );
                                """)
        self.connect_db.commit()


    def close_connection(self) -> None:

        self.connect_db.close()