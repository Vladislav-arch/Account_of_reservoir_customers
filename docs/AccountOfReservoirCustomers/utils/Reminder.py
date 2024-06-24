from datetime import datetime, timedelta
from aiogram import Bot
import asyncio

from data.db.get_profile import get_profile
from data.db.get_last_visit import get_last_visit


class Reminder:
    def __init__(self, tariff, chat_id, bot: Bot, user_id):
        self.tariff = tariff
        self.chat_id = chat_id
        self.bot = bot
        self.user_id = user_id

    async def validity_period_ticket(self):
        if self.tariff == "День":
            now = datetime.now()
            target_time = now.replace(hour=21, minute=00)

            if target_time < now:
                # Якщо вказаний час вже минув у поточному дні, то наступний раз буде наступного дня
                target_time += timedelta(days=1)

            time_left = target_time - now

            print(time_left.total_seconds())
            print(self.chat_id)

            await asyncio.sleep(time_left.total_seconds())

            profile = await get_profile(self.user_id)
            last_visit = await get_last_visit(self.user_id)

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"Кінець дії білету"
                     f"<pre>{profile[2][1]}</pre>"
                     f"{last_visit[0]}")

        elif self.tariff == "Сутки":
            pass
