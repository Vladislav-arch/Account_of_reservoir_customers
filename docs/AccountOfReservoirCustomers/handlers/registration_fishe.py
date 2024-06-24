import asyncio
import re
from contextlib import suppress

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.States import Registration, RegistrationFish
from data.db.table.information_about_fish import insert_information_about_fish
from keyboards.builders import num_kb
from filters.name_is_correct import NameIsCorrect
from utils.UserStorage import UserStorage
from filters.phone_num_is_correct import PhoneNumIsCorrect
from aiogram.exceptions import TelegramBadRequest
from data.db.table.static_information import insert_into_static_information
from data.db.table.dynamic_information import insert_into_dynamic_information
from keyboards import builders
from datetime import date, timedelta
from filters.is_digit_or_float import CheckForDigit
from keyboards import reply
from data.db.get_ids import get_ids
from data.db.get_profile import get_profile
from keyboards import inline
from utils.chat_cleaning import chat_cleaning

router = Router()


@router.message(StateFilter(RegistrationFish.fish_weight, RegistrationFish.trophy_fish,
                            RegistrationFish.photo_of_trophy_fish), F.text == "Назад")
async def form_back(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    user.id_for_secondary_cleaning.append(message.message_id)

    await state.clear()

    await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, user.id_for_secondary_cleaning))

    sent_mess = await message.answer(
        "Операцію скасовано!",
        reply_markup=reply.main
    )
    user.id_for_full_cleanup.append(sent_mess.message_id)


@router.message(RegistrationFish.fish_weight, F.text.isdigit())
async def form_fish_weight(message: Message, state: FSMContext, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_secondary_cleaning.append(message.message_id)
    await state.update_data(fish_weight=message.text)
    await state.set_state(RegistrationFish.trophy_fish)

    mess = await message.answer("Трофейна риба: ", reply_markup=builders.profile(["Немає", "Назад"]))
    user.id_for_secondary_cleaning.append(mess.message_id)


@router.message(RegistrationFish.trophy_fish)
async def form_trophy_fish(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    user.id_for_secondary_cleaning.append(message.message_id)

    if re.match(r'^\d+$', message.text):
        await state.update_data(trophy_fish=message.text)
        await state.set_state(RegistrationFish.photo_of_trophy_fish)
        mess = await message.answer("Надайте фото: ", reply_markup=builders.profile(["Без фото", "Назад"]))
        user.id_for_secondary_cleaning.append(mess.message_id)
    elif message.text == "Немає":
        await state.update_data(trophy_fish=message.text, photo_of_trophy_fish=None)

        await insert_information_about_fish(await state.get_data())

        mess = await message.answer("Готово!", reply_markup=reply.main)
        user.id_for_full_cleanup.id.append(mess.message_id)
        await state.clear()
        await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, user.id_for_secondary_cleaning, 2))
    else:
        mess = await message.answer("Ввдеіть вагу, або натисніть на кнопку!")
        user.id_for_secondary_cleaning.append(mess.message_id)


@router.message(RegistrationFish.photo_of_trophy_fish, F.text == "Без фото")
async def form_no_photo(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    user.id_for_secondary_cleaning.append(message.message_id)
    await state.update_data(photo_of_trophy_fish=None)

    await insert_information_about_fish(await state.get_data())

    mess = await message.answer("Готово!", reply_markup=reply.main)
    user.id_for_full_cleanup.append(mess.message_id)
    await state.clear()
    await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, user.id_for_secondary_cleaning, 2))


@router.message(RegistrationFish.photo_of_trophy_fish, F.photo)
async def form_photo_of_trophy_fish(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    user.id_for_secondary_cleaning.append(message.message_id)

    await state.update_data(photo_of_trophy_fish=message.photo[-1].file_id)

    await insert_information_about_fish(await state.get_data())

    mess = await message.answer("Готово!", reply_markup=reply.main)
    user.id_for_full_cleanup.append(mess.message_id)
    await state.clear()
    await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, user.id_for_secondary_cleaning, 2))


@router.message(RegistrationFish.photo_of_trophy_fish, ~F.photo)
async def incorrect_photo(message: Message, state: FSMContext, users: UserStorage):
    user = users.users_list[message.from_user.id]

    mess = await message.answer("Надайте фото, або натисніть на кнопку!")
    user.id_for_secondary_cleaning.append(mess.message_id)


