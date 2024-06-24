import sqlite3 as sq
from contextlib import suppress

from data.subloader import get_json
from aiogram.exceptions import TelegramBadRequest


async def get_profile(id=None, from_user_id=None):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()
    profile = ""
    select = []

    if id:
        cur.execute(f"SELECT * FROM static_information WHERE id=?", (id,))
        select = cur.fetchone()
        print(select)
    elif from_user_id:
        cur.execute(f"SELECT * FROM static_information WHERE from_user_id=?", (from_user_id,))
        select = cur.fetchone()
        print(select)

    them_profile = await get_json("profile.json")
    for them, data in zip(them_profile, select):
        profile += f"<pre>{str(them[0]) + str(data)}</pre>\n"

    return [profile, select[3], select]