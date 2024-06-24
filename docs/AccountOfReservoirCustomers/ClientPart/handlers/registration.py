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
from ClientPart.utils.States import RegistrationClient
from ClientPart.utils.checker import checker

#data
from data.db.table.static_information import insert_into_static_information

from utils.number_verification import number_verification

router = Router()


@router.message(F.text == "Зареєструватись")
async def fill_profile(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    await state.set_state(RegistrationClient.name)
    await bot.send_message(chat_id=message.chat.id,
                           text="Надайте своє ім'я",
                           reply_markup=builders.profile11(
                               [f"Використати ім`я: {message.from_user.first_name}", "Вийти"])
                           )


@router.message(StateFilter(RegistrationClient.name, RegistrationClient.phone_num), F.text == "Вийти")
async def form_back(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    await state.clear()
    await message.answer(
        "Реєстрацію скасовано!",
        reply_markup=reply.main
    )


@router.message(RegistrationClient.name, NameIsCorrect())
async def form_name(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]

    if message.text[:18] == "Використати ім`я: ":
        name = message.text[18:]
    else:
        name = message.text

    await state.update_data(name=name)
    await state.set_state(RegistrationClient.phone_num)

    await message.answer("Надайте номер телефону",
                         reply_markup=reply.contact)


@router.message(RegistrationClient.phone_num, PhoneNumIsCorrect())
async def form_phone_num(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    contact: Contact = message.contact

    if contact.phone_number:
        phone_number = contact.phone_number
        if phone_number[0] != "+":
            phone_number = '+' + contact.phone_number

    await state.update_data(phone_num=phone_number, photo=None, from_user_id=message.from_user.id)
    data = await state.get_data()
    if await checker(data['phone_num'], "phone_num") and await checker(data['from_user_id'], "from_user_id"):
        await message.answer("Хмм. Схоже ви вже зареєстровані🧐 "
                             "<pre>Ви вже зареєстровані, вам не потрібно більше реєструватись.</pre>",
                             reply_markup=reply.main)
        await state.clear()
        return
    await insert_into_static_information(data)
    await message.answer("Чудово! Ви зареєстровані!☺️\n<pre>Тепер ви зможете бронювати місця ще швидше!</pre>",
                         reply_markup=reply.main)
    await state.clear()

