import sqlite3 as sq


async def checker(data, column, table="static_information", column2=None, data2=None):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    if table == "static_information":
        cur.execute(f"SELECT * FROM static_information WHERE {column} = ?", (data,))
        data = cur.fetchone()
    elif table == "reserved_seats":
        cur.execute(f"SELECT * FROM reserved_seats WHERE {column} = ?", (data,))
        data = cur.fetchone()
    elif table == "reserved_seats2":
        cur.execute(f"SELECT * FROM reserved_seats WHERE {column} = ? AND {column2} = ?", (data, data2))
        data = cur.fetchone()

    print(data)

    if data:
        return True
    return False