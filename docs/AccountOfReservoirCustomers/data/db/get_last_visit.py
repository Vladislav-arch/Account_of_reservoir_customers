import sqlite3 as sq
from data.subloader import get_json


async def get_last_visit(user_id, visit_date=None):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    visit = []

    if visit_date is None:
        cur.execute("""
                SELECT *
                FROM dynamic_information 
                WHERE user_id = ?  
                ORDER BY visit_date DESC
                    """, (user_id,))

        visit = cur.fetchone()
    else:
        cur.execute("""
                SELECT *
                FROM dynamic_information 
                WHERE user_id = ? AND visit_date = ?
                    """, (user_id, visit_date))

        visit = cur.fetchone()

    print(visit)

    if visit is None:
        visit = [" ", "Пусто", "Пусто", "Пусто", "Пусто"]

    them_last_visit = await get_json("last_visit.json")
    last_visit = ""

    for i in range(len(them_last_visit)):
        last_visit += f"<pre>{str(them_last_visit[i][0]) + str(visit[i+1])}</pre>\n"

    return [last_visit, "-------------------------- ------ ----- ---- --- -- -\n<pre>Останнє відвідування:</pre>\n"]
