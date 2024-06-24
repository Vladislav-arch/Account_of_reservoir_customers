import sqlite3 as sq
from data.subloader import get_json


async def update_data(table_name, column_name, new_value, id=None, from_user_id=None):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    if from_user_id:
        print(table_name, column_name, new_value, id, from_user_id)
        cur.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE from_user_id = ?", (new_value, from_user_id))
        db.commit()
        return

    cur.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE id = ?", (new_value, id))
    db.commit()