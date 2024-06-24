import sqlite3 as sq


async def check_from_user_id(from_user_id):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM static_information WHERE from_user_id = ?", (from_user_id,))
    from_user_id = cur.fetchone()

    if from_user_id:
        return True
    return False
