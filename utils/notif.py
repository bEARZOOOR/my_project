from aiogram import Bot
from config_data.config import load_config, Config
from database.database import DatabaseManager

import datetime
import asyncio


config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode="html")
db_manager: DatabaseManager = DatabaseManager()
cursor = db_manager.connect_db.cursor()

date_notif = None
date_payment = None


async def take_date(sec:int = 24*60*60):
    global date_notif
    while True:
        now = datetime.datetime.now()
        with_add_days = datetime.timedelta(days=4)
        notification = (now + with_add_days).strftime("%d/%m/%y")
        date_notif = tuple(notification.split())
        await asyncio.sleep(sec)


        
async def take_dates_from_db(sec:int = 24*60*60): # проверка на совпадение
    global date_payment
    while True:
        cursor = db_manager.connect_db.cursor()
        query = """
                SELECT date_payment
                FROM finance
                WHERE reg_payment == 0
                """
        date_payment = cursor.execute(query).fetchall()
        await asyncio.sleep(sec)



async def date_check(sec:int = 24*60*60) -> str:
    global date_notif
    global date_payment
    chat_id = config.tg_bot.admin_ids
    while True:
        if date_notif is not None and date_payment is not None:
            if date_notif in date_payment:
                query = """
                        SELECT auto.rowid, auto.full_name, auto.phone
                        FROM finance
                        JOIN auto ON finance.user_id == auto.rowid
                        WHERE date_payment == "{}"
                        """.format(date_notif[0])
                info = cursor.execute(query).fetchall()
                show_info = f"id: {info[0][0]}\nФИО: {info[0][1]}\nтелефон: {info[0][2]}"
                for id in chat_id:
                    await bot.send_message(id, text=show_info)
                await asyncio.sleep(sec)
            else:
                print("Напоминания [ВКЛ]")
                await asyncio.sleep(sec)




async def start_notifications():
    task1 = asyncio.create_task(take_date())
    task2 = asyncio.create_task(take_dates_from_db())
    task3 = asyncio.create_task(date_check())

    await asyncio.gather(task1, task2, task3)