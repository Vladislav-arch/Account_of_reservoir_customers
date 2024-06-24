import sqlite3 as sq


async def check_date(visit_date):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM dynamic_information WHERE visit_date = ?", (visit_date,))
    visit_date = cur.fetchone()

    if visit_date:
        return True
    return False