import sqlite3 as sq

from data.db.table.static_information import create_static_information
from data.db.table.dynamic_information import create_dynamic_information
from data.db.table.information_about_fish import create_information_about_fish
from data.db.table.reserved_seats import create_reserved_seats
from data.db.table.photos import create_photos


async def start_db():
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    await create_static_information()
    await create_dynamic_information()
    await create_information_about_fish()
    await create_reserved_seats()
    await create_photos()

    db.close()
