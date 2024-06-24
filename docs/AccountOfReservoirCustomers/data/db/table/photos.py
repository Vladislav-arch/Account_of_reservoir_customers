import sqlite3 as sq
from aiogram.fsm.context import FSMContext
from data.db.get_ids import get_ids


async def create_photos():
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS information_about_fish (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place text,
        file_id TEXT NOT NULL,
        file_unique_id TEXT NOT NULL,
        file_path TEXT NOT NULL
    )""")


async def insert_photos(place, file_id, file_unique_id, file_path):
    print(data)

    cur.execute(
        "INSERT INTO information_about_fish(place, file_id, file_unique_id, file_path) VALUES (?, ?, ?, ?)",
        (data['place'], data['file_id'], data['file_unique_id'], data['file_path'])
    )
    db.commit()

