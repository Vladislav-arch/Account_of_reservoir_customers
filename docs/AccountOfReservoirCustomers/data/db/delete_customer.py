import sqlite3 as sq


async def delete_customer(id):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"DELETE FROM static_information WHERE id = {id}")
    cur.execute(f"DELETE FROM dynamic_information WHERE user_id = {id}")
    cur.execute(f"DELETE FROM information_about_fish WHERE user_id = {id}")

    db.commit()
