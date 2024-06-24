import sqlite3 as sq


async def checking_reserved_seats(place, day):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM reserved_seats WHERE place = ? AND day = ?", (place, day,))
    data = cur.fetchone()

    print(data)

    if data:
        return True
    return False