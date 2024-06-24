from datetime import datetime
import sqlite3 as sq


async def check_datetime_passed():
    global db, cur
    input_date = ""
    input_time = ""
    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM reserved_seats")
    data = cur.fetchall()

    print(data)

    ids = []

    for d in data:
        print(d[1])
        current_datetime = datetime.now()
        input_datetime = datetime.strptime(d[1] + " " + d[3], "%Y-%m-%d %H:%M")

        if input_datetime <= current_datetime:
            print("Цей день і час вже пройшли.")
            ids.append(d[0])
        else:
            print("Цей день і час ще не пройшли.")

    for id in ids:
        cur.execute(f"DELETE FROM reserved_seats WHERE id = ?", (id,))
        db.commit()
