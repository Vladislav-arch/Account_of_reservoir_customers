import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

#router
from ClientPart.handlers import registration, user_commands, reserve_seat, profile
from ClientPart.callback import registration_offer_call, reserve_seat_call, profile_call

#utils
from ClientPart.utils.UserStorage import UserStorage


async def main():
    bot = Bot("7252051562:AAGzfQtsfiPEd5wyk5oPgWyB-X47dKdC_PM", default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    users = UserStorage
    #dp.message.middleware(AntiFloodMidleware())

    dp.include_routers(
        user_commands.router,
        registration_offer_call.router,
        profile_call.router,
        registration.router,
        reserve_seat_call.router,
        reserve_seat.router,
        profile.router,

    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, users=users)


if __name__ == "__main__":
    asyncio.run(main())
