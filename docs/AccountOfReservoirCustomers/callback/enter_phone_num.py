from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from contextlib import suppress
import asyncio

from utils.UserStorage import UserStorage
from utils.States import Registration, ReserveSeat
from keyboards.builders import num_kb
from data.db.table.reserved_seats import insert_reserved_seats
from utils.Places import Places
from utils.number_verification import number_verification
from keyboards import builders
from utils.number_verification import number_verification

import phonenumbers

router = Router()


@router.callback_query(ReserveSeat.user_phone, F.data == "OK")
async def enter_phone_num(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    p = Places(callback.message.chat.id, bot)

    if callback.data == "OK" and await validate_phone_number(user.phone_number):
        await state.update_data(user_phone=user.phone_number, name="")
        data = await state.get_data()

        await insert_reserved_seats(data)

        sent_mess = await bot.send_message(chat_id=callback.message.chat.id, text="Готово")
        user.id_for_full_cleanup.append(sent_mess.message_id)

        if not await number_verification(data['user_phone']):
            sent_mess = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=f"<pre>Номер {data['user_phone']} не зареєстрований в системі. Зареєструвати?</pre>",
                reply_markup=builders.profile_inline(["Зареєструвати", "Потім"])
            )
            user.temp_mess_id = sent_mess.message_id
            user.id_for_full_cleanup.append(sent_mess.message_id)

        await state.clear()
        await asyncio.create_task(p.delete_automatically(data))


@router.callback_query(Registration.phone_num, F.data == "OK")
async def enter_phone_num(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    if await number_verification(user.phone_number):
        await callback.answer("Даний номер уже зареєстровано в системі!")
    elif not await validate_phone_number(user.phone_number):
        await callback.answer("Номер не є коректним!")
    elif callback.data == "OK":
        await state.update_data(phone_num=user.phone_number)
        await state.set_state(Registration.photo)
        sent_mess = await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Надайте фото: "
        )
        user.id_for_full_cleanup.append(sent_mess.message_id)

    await callback.answer()


@router.callback_query(StateFilter(Registration.phone_num, ReserveSeat.user_phone))
async def enter_phone_num(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    items = [
        "1", "2", "3",
        "4", "5", "6",
        "7", "8", "9",
        "0"
    ]

    for item in items:
        if item == callback.data and len(user.phone_number) <= 12:
            user.phone_number += item

    if callback.data == "❌" and len(user.phone_number) >= 5:
        user.phone_number = user.phone_number[:-1]

    with suppress(TelegramBadRequest):
        sent_mess = await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            text=f"Надайте номер телефону: {user.phone_number}",
            message_id=callback.message.message_id,
            reply_markup=num_kb()
        )
        user.id_for_full_cleanup.append(sent_mess.message_id)
    await callback.answer()


async def validate_phone_number(phone_number):
    try:
        phone_number_object = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(phone_number_object)
    except phonenumbers.NumberParseException as e:
        return False

