import sqlite3 as sq
import re

from aiogram.fsm.context import FSMContext
from data.db.get_ids import get_ids


async def create_reserved_seats():
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS reserved_seats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day date NOT NULL,
        place varchar,
        start_time TIME,
        user_phone varchar,
        name varchar


    )""")


async def insert_reserved_seats(data):
    print(data)

    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    if not data['name']:
        data['name'] = None

    cur.execute(
        "INSERT INTO reserved_seats(day, place, start_time, user_phone, name)"
        "VALUES (?, ?, ?, ?, ?)",
        (data['day'], data['place'], data['start_time'], data['user_phone'], data['name'])
    )
    db.commit()


async def delete_reservation(data):
    print(data['user_phone'])
    cur.execute(f"DELETE FROM reserved_seats WHERE user_phone = ?", (data['user_phone'],))
    db.commit()


async def delete_reserve(data):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    # Шукаємо патерн дати і часу у тексті
    pattern = r'^(.*?): (\d{4}-\d{2}-\d{2}) - (\d{2}:\d{2})$'
    match = re.match(pattern, data["date"])

    if match:
        place = match.group(1)
        date = match.group(2)
        time = match.group(3)
    else:
        raise ValueError("Невірний формат тексту. Потрібно 'Місце: рік-місяць-день - година:хвилина'.")

    cur.execute(f"DELETE FROM reserved_seats WHERE day = ? AND place = ? AND start_time = ?", (date, place, time))
    db.commit()



