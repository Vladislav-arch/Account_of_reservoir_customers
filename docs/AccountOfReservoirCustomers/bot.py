import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers import (user_commands, registration, customers, edit_profile, customer_search,
                      registration_fishe, places, change_photos_of_seats)
from Midleware.antiflood import AntiFloodMidleware
from data.db.start_db import start_db
from utils.UserStorage import UserStorage
from callback import enter_phone_num, context_menu, enter_visit_date, places_call


async def on_startup(_):
    await start_db()


async def main():
    bot = Bot("6577823184:AAF3j5kN3moSgtWiQceewDxXO9BnNY_vxKg", default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    users = UserStorage
    dp.message.middleware(AntiFloodMidleware())

    dp.include_routers(
        user_commands.router,
        enter_phone_num.router,
        enter_visit_date.router,
        context_menu.router,
        places_call.router,
        registration.router,
        change_photos_of_seats.router,
        registration_fishe.router,
        customer_search.router,
        edit_profile.router,
        customers.router,
        places.router,
    )

    await start_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, users=users)


if __name__ == "__main__":
    asyncio.run(main())
