import asyncio
from contextlib import suppress

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.States import SearchCustomer
from utils.States import Registration
from keyboards.builders import num_kb
from filters.name_is_correct import NameIsCorrect
from utils.UserStorage import UserStorage
from filters.phone_num_is_correct import PhoneNumIsCorrect
from aiogram.exceptions import TelegramBadRequest
from data.db.table.static_information import insert_into_static_information
from data.db.table.dynamic_information import insert_into_dynamic_information
from keyboards import builders
from datetime import date, timedelta
from filters.visit_date_is_correct import VisitDateIsCorrect
from keyboards import reply
from data.db.get_ids import get_ids
from data.db.get_profile import get_profile
from keyboards import inline
from data.db.search import search
from utils.chat_cleaning import chat_cleaning

router = Router()


@router.message(F.text == "Пошук")
async def customer_search(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)
    await chat_cleaning(user, bot, message.chat.id, user.id_for_full_cleanup)
    mess = await message.answer("Пошук", reply_markup=reply.main)
    user.id_for_full_cleanup.append(mess.message_id)

    await state.set_state(SearchCustomer.search)
    mess = await message.answer(
        "Введіть дані для пошуку.",
        reply_markup=builders.profile("Назад"))
    user.id_for_full_cleanup.append(mess.message_id)


@router.message(StateFilter(SearchCustomer.search), F.text == "Назад")
async def form_back(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)

    await state.clear()

    await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, user.id_for_full_cleanup))

    mess = await message.answer(
        "Операцію скасовано!",
        reply_markup=reply.main
    )
    user.id_for_full_cleanup.append(mess.message_id)


@router.message(SearchCustomer.search)
async def customer_search(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    id = await search(message.text)

    if id is not None:
        await state.clear()
        data = await get_profile(id[0])

        mess = await bot.send_photo(
            chat_id=message.chat.id,
            photo=data[1],
            caption=data[0],
            reply_markup=inline.context

        )
        user.id_for_full_cleanup.append(mess.message_id)
    else:
        mess = await message.answer("Нікого не знайдено.",
                                    reply_markup=reply.main)
        user.id_for_full_cleanup.append(mess.message_id)
        return
    mess = await message.answer("Результат пошуку",
                                reply_markup=reply.main)
    user.id_for_full_cleanup.append(mess.message_id)
