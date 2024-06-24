from __future__ import annotations

import asyncio

from aiogram import Bot


async def chat_cleaning(user: object, bot: Bot, chat_id: int, message_id: int | list, sleep=0):
    await asyncio.sleep(sleep)

    """
    Функція для видалення повідомлення за його ID.

    Args:
        bot (aiogram.Bot): Екземпляр бота Aiogram.
        chat_id (int): ID чату, в якому знаходиться повідомлення.
        message_id (int): ID повідомлення, яке потрібно видалити.
    """
    if isinstance(message_id, int):
        message_id = [message_id]

    for id in message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=id)
        except Exception as e:
            print(f"Помилка при видаленні повідомлення: {e}")

    user.id_for_full_cleanup = []