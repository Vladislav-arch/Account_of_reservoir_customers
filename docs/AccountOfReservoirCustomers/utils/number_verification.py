import sqlite3 as sq


async def number_verification(phone_number):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM static_information WHERE phone_num = ?", (phone_number,))
    phone_num = cur.fetchone()

    if phone_num:
        return True
    return False
