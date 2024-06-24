from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Contact
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from contextlib import suppress
import asyncio

from data.db.get_profile import get_profile
from data.db.table.static_information import insert_into_static_information

#utils
from ClientPart.utils.UserStorage import UserStorage
from ClientPart.utils.States import RegistrationClient, Profile
from utils.number_verification import number_verification

#keyboards
from ClientPart.keyboards import builders
from ClientPart.keyboards import reply

#data
from data.db.update_data import update_data

import phonenumbers

router = Router()


@router.callback_query(Profile.edit_profile, F.data.in_(['Назад', ]))
async def enter_phone_num(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    data = await get_profile(from_user_id=callback.from_user.id)
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=user.temp_mess_id,
                                text=data[0],
                                reply_markup=builders.profile_inline(["Редагувати дані"]))
    await state.set_state(Profile.profile)


@router.callback_query(Profile.profile, F.data.in_(['Редагувати дані', ]))
async def enter_phone_num(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=user.temp_mess_id,
                                        reply_markup=builders.profile_inline11(
                                            ["Змінити ім`я", "Змінити номер телефону", "Назад"]))
    await state.set_state(Profile.edit_profile)


@router.callback_query(Profile.edit_profile, F.data.in_(['Змінити ім`я', "Змінити номер телефону"]))
async def enter_phone_num(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    if callback.data == "Змінити ім`я":
        await callback.message.answer("Надайте нове  ім`я",
                                      reply_markup=builders.profile11(
                                          [f"Використати ім`я: {callback.from_user.first_name}", "Вийти"]))
        await state.set_state(Profile.name)
    elif callback.data == "Змінити номер телефону":
        await callback.message.answer("Надайте новий номер телефону",
                                      reply_markup=reply.contact)
        await state.set_state(Profile.phone)


