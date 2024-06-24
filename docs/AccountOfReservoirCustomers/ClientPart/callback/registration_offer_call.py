from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from contextlib import suppress
import asyncio
from data.db.table.static_information import insert_into_static_information

#utils
from ClientPart.utils.UserStorage import UserStorage
from ClientPart.utils.States import RegistrationClient
from utils.number_verification import number_verification

#keyboards
from ClientPart.keyboards import builders
from ClientPart.keyboards import reply


import phonenumbers

router = Router()


@router.callback_query(F.data.in_(['Бажаю', 'Потім']))
async def enter_phone_num(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]

    if callback.data == "Бажаю":
        await callback.message.answer("Чудово!😌")
        await state.set_state(RegistrationClient.name)
        await callback.message.answer(text="Надайте своє ім'я: ", reply_markup=builders.profile11(
            [f"Використати ім`я: {callback.from_user.first_name}", "Назад"]))
    elif callback.data == "Потім":
        await callback.message.answer("Добре. Я вам потім нагадаю.😔")
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)


