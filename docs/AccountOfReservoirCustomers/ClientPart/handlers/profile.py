import asyncio
from contextlib import suppress

from aiogram import Router, F, Bot, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import Message, Contact
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Contact

#keyboard
from ClientPart.keyboards import builders
from ClientPart.keyboards import reply

#filters
from ClientPart.filters.name_is_correct import NameIsCorrect
from ClientPart.filters.phone_num_is_correct import PhoneNumIsCorrect

#utils
from ClientPart.utils.UserStorage import UserStorage
from ClientPart.utils.States import RegistrationClient, Profile
from ClientPart.utils.checker import checker

#data
from data.db.table.static_information import insert_into_static_information
from data.db.get_profile import get_profile
from data.db.update_data import update_data

from utils.number_verification import number_verification

router = Router()


@router.message(StateFilter(Profile.name, Profile.phone), F.text == "Вийти")
async def fill_profile(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]

    data = await get_profile(from_user_id=message.from_user.id)
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=user.temp_mess_id,
                                text=data[0],
                                reply_markup=builders.profile_inline(["Редагувати дані"]))
    await message.answer("Операцію скасовано!", reply_markup=reply.main)
    await state.set_state(Profile.profile)


@router.message(F.text == "Мій профіль")
async def fill_profile(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    await state.set_state(Profile.profile)
    data = await get_profile(from_user_id=message.from_user.id)

    mess = await message.answer(text=data[0],
                                reply_markup=builders.profile_inline(["Редагувати дані"]))
    user.temp_mess_id = mess.message_id


@router.message(Profile.name)
async def enter_phone_num(message: Message, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[message.from_user.id]

    if message.text[:18] == "Використати ім`я: ":
        name = message.text[18:]
    else:
        name = message.text

    await update_data("static_information", "name", name, from_user_id=message.from_user.id)

    data = await get_profile(from_user_id=message.from_user.id)
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=user.temp_mess_id,
                                text=data[0],
                                reply_markup=builders.profile_inline(["Редагувати дані"]))
    await message.answer("Готово! Ім`я змінено!", reply_markup=reply.main)
    await state.set_state(Profile.profile)


@router.message(Profile.phone)
async def enter_phone_num(message: Message, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[message.from_user.id]
    contact: Contact = message.contact

    if contact.phone_number:
        phone_number = contact.phone_number
        if phone_number[0] != "+":
            phone_number = '+' + contact.phone_number

    await update_data("static_information", "phone_num", phone_number, from_user_id=message.from_user.id)

    data = await get_profile(from_user_id=message.from_user.id)
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=user.temp_mess_id,
                                text=data[0],
                                reply_markup=builders.profile_inline(["Редагувати дані"]))
    await  message.answer("Готово! Номер телефону змінено!", reply_markup=reply.main)
    await state.set_state(Profile.profile)
