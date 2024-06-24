import sqlite3 as sq
from data.subloader import get_json


async def get_result_of_the_last_visit(id, date):
    global db, cur

    db = sq.connect('customers.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM  information_about_fish WHERE user_id=? AND user_visit_date = ? ", (id, date))
    result = cur.fetchone()
    print(f"----------{result}")

    if result is None:
        result = None
        return result

    them_result_of_the_last_visit = await get_json("result_of_the_last_visit.json")
    last_res = ""

    for i in range(len(them_result_of_the_last_visit)):
        last_res += f"<pre>{str(them_result_of_the_last_visit[i][0]) + str(result[i+1])}</pre>\n"

    return [result[4], last_res]