import sqlite3 as sq
from data.subloader import get_json


async def get_reserved_seats():
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM reserved_seats")
    data = cur.fetchall()

    print(data)

    return data



