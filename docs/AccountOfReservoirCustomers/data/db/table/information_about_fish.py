import sqlite3 as sq
from aiogram.fsm.context import FSMContext
from data.db.get_ids import get_ids


async def create_information_about_fish():
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS information_about_fish (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_visit_date date NOT NULL,
        fish_weight float,
        trophy_fish float,
        photo_of_trophy_fish text,
        user_id BIGINT NOT NULL,

        CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES static_information (id)
        CONSTRAINT user_visit_date_fk FOREIGN KEY (user_visit_date) REFERENCES dynamic_information (visit_date)
    )""")


async def insert_information_about_fish(data):
    print(data)

    cur.execute(
        "INSERT INTO information_about_fish(user_visit_date, fish_weight, trophy_fish, photo_of_trophy_fish, "
        "user_id) VALUES (?, ?, ?, ?, ?)",
        (data['visit_date'], data['fish_weight'], data['trophy_fish'], data['photo_of_trophy_fish'], data['user_id'])
    )
    db.commit()

