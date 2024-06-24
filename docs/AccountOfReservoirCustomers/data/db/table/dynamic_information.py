import sqlite3 as sq
from aiogram.fsm.context import FSMContext
from data.db.get_ids import get_ids


async def create_dynamic_information():
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS dynamic_information (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visit_date date,
        tariff text,
        fishing_place text,
        user_id BIGINT NOT NULL,
        
        CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES static_information (id)
    )""")


async def insert_into_dynamic_information(data):
    print(data)

    cur.execute(
        "INSERT INTO dynamic_information(visit_date, tariff, fishing_place, user_id) VALUES (?, ?, ?, ?)",
        (data['visit_date'], data['tariff'], data['fishing_place'], data['user_id'])
    )
    db.commit()

