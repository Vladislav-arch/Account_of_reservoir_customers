import asyncio
from datetime import date

from aiogram import Router, F, Bot
from utils import UserStorage
from aiogram.types import Message
from data.db.get_ids import get_ids
from data.db.get_profile import get_profile
from keyboards import inline, reply, builders
from utils.chat_cleaning import chat_cleaning
from utils.Places import Places
from aiogram.fsm.context import FSMContext
from utils.States import ReserveSeat
from filters.is_valid_time import ІsValidTime


router = Router()


@router.message(F.text == "Місця")
async def places(message: Message, bot: Bot, users: UserStorage, state: FSMContext):
    p = Places(message.chat.id, bot)
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)
    await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, user.id_for_full_cleanup, 0))
    await message.answer("Місця", reply_markup=reply.main)

    await state.set_state(ReserveSeat.day)

    await p.get_places(user)


@router.message(ReserveSeat.start_time, ІsValidTime())
async def start_time(message: Message, bot: Bot, users: UserStorage, state: FSMContext):
    await state.update_data(start_time=message.text)

    user = users.users_list[message.from_user.id]
    await state.update_data(end_time=message.text)

    await state.set_state(ReserveSeat.user_phone)

    sents_mess = await message.answer(
        f"Надайте номер телефону: {user.phone_number}",
        reply_markup=builders.num_kb()
    )
    user.temp_mess_id = sents_mess.message_id
    user.id_for_full_cleanup.append(sents_mess.message_id)
