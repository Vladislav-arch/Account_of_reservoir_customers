import sqlite3 as sq


async def get_ids(date=None):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    if date is None:
        cur.execute('SELECT id FROM static_information')
        ids = cur.fetchall()
        return ids
    elif date:
        cur.execute(f"SELECT user_id FROM dynamic_information WHERE visit_date=?", (date,))
        ids = cur.fetchall()
        return ids

