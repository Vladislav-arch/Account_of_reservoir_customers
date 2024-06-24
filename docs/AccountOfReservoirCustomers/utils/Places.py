from contextlib import suppress
from datetime import datetime, timedelta, date

from aiogram import Bot
import asyncio

from aiogram.exceptions import TelegramBadRequest

from data.db.get_profile import get_profile
from data.db.get_last_visit import get_last_visit
import sqlite3 as sq
from keyboards import builders
from keyboards.builders import profile_inline
from data.db.table.reserved_seats import insert_reserved_seats
from data.db.table.reserved_seats import delete_reservation


class Places:
    DAYS = ["❌" ,f"{date.today()}", f"{date.today() + timedelta(days=1)}", f"{date.today() + timedelta(days=2)}",
            f"{date.today() + timedelta(days=3)}", f"{date.today() + timedelta(days=4)}",
            f"{date.today() + timedelta(days=5)}",
            f"{date.today() + timedelta(days=6)}"]
    PLACES = ["Місце 1", "Місце 2", "Місце 3", "Місце 4"]

    def __init__(self, chat_id, bot: Bot):
        self.chat_id = chat_id
        self.bot = bot

    async def get_places(self, user, state=None):
        global db, cur

        db = sq.connect('customers.db')
        cur = db.cursor()

        cur.execute(f"SELECT * FROM reserved_seats")
        data = cur.fetchall()

        text = ""

        print(text)

        if not data:
            text = "<pre>Всі дні вільні</pre>"
        else:
            print(data)
            for d in data:
                text += f"<pre>{d[2]}: {d[1]} - бронь {d[3]}({d[4]})\n</pre>"

        if state is None:
            sent_mess = await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                reply_markup=builders.days(self.DAYS)
            )
            user.temp_mess_id = sent_mess.message_id
            user.id_for_full_cleanup.append(sent_mess.message_id)
        elif state == "back":
            sent_mess = await self.bot.edit_message_text(
                chat_id=self.chat_id,
                message_id=user.temp_mess_id,
                text=text,
                reply_markup=builders.days(self.DAYS)
            )
            user.temp_mess_id = sent_mess.message_id
            user.id_for_full_cleanup.append(sent_mess.message_id)

    async def free_seats_for_the_current_day(self, day, user):
        cur.execute(f"SELECT * FROM reserved_seats WHERE day = ? ", (day,))
        data = cur.fetchall()

        text = ""

        for p in self.PLACES:
            for d in data:
                if p == d[2]:
                    text += f"<pre>{p}(бронь)</pre>\n"
                    continue
            text += f"<pre>{p}(вільно)</pre>\n"

        sent_mess = await self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=user.temp_mess_id,
            text=text,
            reply_markup=profile_inline(["Місце 1", "Місце 2", "Місце 3", "Місце 4", "Назад"])
        )
        user.id_for_full_cleanup.append(sent_mess.message_id)

    async def place_information(self, place, day, user):
        cur.execute(f"SELECT start_time, user_phone FROM reserved_seats WHERE place = ? AND day = ?",
                    (place, day))
        data = cur.fetchall()
        print(data)

        text = ""

        if data:
            for d in data:
                text += f"<pre>{d[1]} - бронь на {d[0]}</pre>"
        else:
            text = "<pre>Вільно протягом дня</pre>"

        sent_mess = await self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=user.temp_mess_id,
            text=f"{text}",
            reply_markup=profile_inline([f"Забронювати {place}", "Назад"])
        )
        user.temp_mess_id = sent_mess.message_id
        user.id_for_full_cleanup.append(sent_mess.message_id)

    async def reserve_a_seat(self, data):
        await insert_reserved_seats(data)

    async def delete_automatically(self, data, client=None, admin=None):
        now = datetime.now()

        # Дата і час вказаного дня і часу
        target_datetime_str = f"{data['day']} {data['start_time']}"
        target_datetime = datetime.strptime(target_datetime_str, "%Y-%m-%d %H:%M")

        # Якщо вказаний час вже пройшов сьогодні, перехід на наступний день
        if target_datetime < now:
            target_datetime += timedelta(days=1)

        # Різниця між вказаним часом і поточним часом
        difference = target_datetime - now
        print(difference.total_seconds())
        await asyncio.sleep(int(difference.total_seconds()))

        if admin:
            sent_mess = await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"<pre>У вас на {data['start_time']} заброньоване місце</pre>"
                     f"<pre>Телефон: {data['user_phone']}</pre>",
                reply_markup=profile_inline("Зрозуміло")
            )
        elif client:
            sent_mess = await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"<pre>У вас на {data['start_time']} заброньоване місце</pre>",
                reply_markup=profile_inline("Зрозуміло")
            )

        with suppress(TelegramBadRequest):
            await delete_reservation(data)


