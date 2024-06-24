from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from contextlib import suppress

from keyboards import reply, builders
from utils.UserStorage import UserStorage
from utils.States import Registration, DeleteReserve
from keyboards.builders import num_kb
from utils.States import ReserveSeat
from utils.Places import Places
from data.db.get_reserved_seats import get_reserved_seats
from data.db.table.reserved_seats import delete_reserve

import phonenumbers

from utils.chat_cleaning import chat_cleaning

router = Router()


@router.callback_query(DeleteReserve.data_to_delete, F.data == "Назад")
async def place_back(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    p = Places(callback.message.chat.id, bot)
    await p.get_places(user, "back")
    await state.set_state(ReserveSeat.day)


@router.callback_query(ReserveSeat.day, F.data == "❌")
async def place_back(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    await callback.answer("Оберіть день який ви хочите видалить")

    data = await get_reserved_seats()
    keyboard = []
    for d in data:
        keyboard.append(f"{d[2]}: {d[1]} - {d[3]}")
    keyboard.append("Назад")

    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=builders.profile_inline(keyboard))
    await state.set_state(DeleteReserve.data_to_delete)


@router.callback_query(DeleteReserve.data_to_delete)
async def place_back(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    await state.update_data(date=callback.data)

    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=builders.profile_inline(["Видалити", "Не видаляти"]))
    await state.set_state(DeleteReserve.yes_or_no)


@router.callback_query(DeleteReserve.yes_or_no)
async def place_back(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    p = Places(callback.message.chat.id, bot)

    if callback.data == "Видалити":
        with suppress(TelegramBadRequest):
            await delete_reserve(await state.get_data())
        await callback.answer("Бронювання видалено")
        p = Places(callback.message.chat.id, bot)
        await p.get_places(user, "back")
        await state.set_state(ReserveSeat.day)
        return
    elif callback.data == "Не видаляти":
        data = await get_reserved_seats()
        keyboard = []
        for d in data:
            keyboard.append(f"{d[2]}: {d[1]} - {d[3]}")
        keyboard.append("Назад")

        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            reply_markup=builders.profile_inline(keyboard))
        await state.set_state(DeleteReserve.data_to_delete)


@router.callback_query(ReserveSeat.place, F.data == "Назад")
async def place_back(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    p = Places(callback.message.chat.id, bot)

    await state.set_state(ReserveSeat.day)

    await p.get_places(user, "back")


@router.callback_query(ReserveSeat.reserve_seat, F.data == "Назад")
async def place_back(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    p = Places(callback.message.chat.id, bot)

    await state.set_state(ReserveSeat.place)

    await p.get_places(user, "back")

    data = await state.get_data()
    print(data)
    await p.free_seats_for_the_current_day(data['day'], user)


@router.callback_query(ReserveSeat.day)
async def days(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    p = Places(callback.message.chat.id, bot)
    await state.set_state(ReserveSeat.place)
    await state.update_data(day=f"{callback.data}")

    await p.free_seats_for_the_current_day(callback.data, user)


@router.callback_query(ReserveSeat.place)
async def place(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    p = Places(callback.message.chat.id, bot)
    data = await state.get_data()
    await state.update_data(place=f"{callback.data}")

    await state.set_state(ReserveSeat.reserve_seat)

    await p.place_information(callback.data, data['day'], user)


@router.callback_query(ReserveSeat.reserve_seat)
async def reserve_seat(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    sent_mess = await callback.message.answer("Надайте час початку: ")
    user.id_for_full_cleanup.append(sent_mess.message_id)

    await state.set_state(ReserveSeat.start_time)


@router.callback_query(F.data == "Зрозуміло")
async def well(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=user.temp_mess_id)


@router.callback_query(F.data.in_(["Зареєструвати", "Потім"]))
async def well(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    if callback.data == "Зареєструвати":
        user.id_for_full_cleanup.append(callback.message.message_id)
        await chat_cleaning(user, bot, callback.message.chat.id, user.id_for_full_cleanup, 0)
        await callback.message.answer("Зареєструвати", reply_markup=reply.main)

        await state.set_state(Registration.name)
        await state.update_data(id=None)
        sent_mess = await callback.message.answer(text="Надайте ім'я: ", reply_markup=builders.profile("Назад"))
        user.id_for_full_cleanup.append(sent_mess.message_id)
    elif callback.data == "Потім":
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=user.temp_mess_id)