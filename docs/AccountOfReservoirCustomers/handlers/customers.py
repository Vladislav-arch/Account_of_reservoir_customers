import asyncio
from datetime import date

from aiogram import Router, F, Bot, exceptions
from utils import UserStorage
from aiogram.types import Message
from data.db.get_ids import get_ids
from data.db.get_profile import get_profile
from keyboards import inline, reply
from utils.chat_cleaning import chat_cleaning


router = Router()


@router.message(F.text == "Клієнти")
async def customers(message: Message, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)
    await chat_cleaning(user, bot, message.chat.id, user.id_for_full_cleanup)
    sent_mess = await message.answer("Клієнти", reply_markup=reply.main)
    user.id_for_full_cleanup.append(sent_mess.message_id)

    ids = await get_ids()
    if ids:
        for id in ids:
            data = await get_profile(id[0])
            sent_mess = await bot.send_photo(
                chat_id=message.chat.id,
                photo=data[1],
                caption=data[0],
                reply_markup=inline.context
            )
            user.id_for_full_cleanup.append(sent_mess.message_id)
    else:
        sent_mess = await message.answer("Покищо пусто.")
        user.id_for_full_cleanup.append(sent_mess.message_id)


@router.message(F.text == "Клієнти за сьогодні")
async def customers(message: Message, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)
    await chat_cleaning(user, bot, message.chat.id, user.id_for_full_cleanup)
    sent_mess = await message.answer("Клієнти за сьогодні", reply_markup=reply.main)
    user.id_for_full_cleanup.append(sent_mess.message_id)

    ids = await get_ids(date.today())
    if ids:
        for id in ids:
            data = await get_profile(id[0])
            sent_mess = await bot.send_photo(
                chat_id=message.chat.id,
                photo=data[1],
                caption=data[0],
                reply_markup=inline.context
            )
            user.id_for_full_cleanup.append(sent_mess.message_id)
    else:
        sent_mess = await message.answer("Покищо пусто.")
        user.id_for_full_cleanup.append(sent_mess.message_id)