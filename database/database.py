import sqlite3


class DatabaseManager:
    db_path = "./database/license.db"
    connect_db = sqlite3.connect(db_path)


    async def create_table(self) -> None:

        self.connect_db.execute("""
                    CREATE TABLE IF NOT EXISTS license(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT,
                    phone TEXT,
                    brand TEXT,
                    model TEXT,
                    year TEXT,
                    color TEXT,
                    license_numb TEXT);
                                """)
                                
            
        self.connect_db.commit()


    async def close_connection(self) -> None:

        self.connect_db.close()
'''
db_manager: DatabaseManager = DatabaseManager()

cursor = db_manager.connect_db.cursor()
query = "SELECT * FROM license"
id = ""
for i in cursor.execute(query):
    id,full_name,phone,brand,model,year,color,license_numb=i

    print(f'ФИО: {full_name}\n')
    print(f'Телефон: {phone}\n')
    print(f'Марка: {brand}\n')
    print(f'Модель: {model}\n')
    print(f'Год выпуска: {year}\n')
    print(f'Цвет: {color}\n')
    print(f'Гос.номер: {license_numb}\n')
    #print(id)
id = ""
print(id == True)
'''   
