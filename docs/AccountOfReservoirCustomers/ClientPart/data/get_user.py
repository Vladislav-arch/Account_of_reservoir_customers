import sqlite3 as sq


async def get_user(from_user_id):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM static_information WHERE from_user_id = ?", (from_user_id,))
    from_user_id = cur.fetchone()
    print(from_user_id)
    print("5325")

    return from_user_id
