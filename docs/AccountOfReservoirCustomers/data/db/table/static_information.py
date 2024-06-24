import sqlite3 as sq




async def create_static_information():
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS static_information (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        phone_num varchar,   
        photo varchar,
        from_user_id varchar
    )""")


async def insert_into_static_information(data):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    print(data)

    if not data['photo']:
        data['photo'] = "AgACAgIAAxkBAAIMOWZt93KYiX6ixPhWosZ_rAF6HZ5XAAKh3jEbsdVwSyejnZvuH5FzAQADAgADeAADNQQ"

    if not data['from_user_id']:
        data['from_user_id'] = "Зареєстровано з admin"

    print(data)
    cur.execute(
        "INSERT INTO static_information(name, phone_num, photo, from_user_id) VALUES (?, ?, ?, ?)",
        (data['name'], data['phone_num'], data['photo'], data['from_user_id'])
    )
    db.commit()


async def update_into_static_information(column, where, search_data, set_data):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(
            f"UPDATE static_information SET {column} = ? WHERE {where} = ?", (set_data, search_data,)
    )
    db.commit()

