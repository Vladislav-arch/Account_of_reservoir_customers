import sqlite3 as sq
from data.subloader import get_json


async def search(data):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    columns = ["id", "name", "phone_num", "photo"]
    id = ""

    for column in columns:
        cur.execute(f"SELECT id FROM static_information WHERE {column}=?", (data,))
        id = cur.fetchone()
        if id is not None:
            return id
    return None


