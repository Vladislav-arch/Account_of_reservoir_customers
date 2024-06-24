from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

from data.db.get_last_visit import get_last_visit
from data.db.get_profile import get_profile
from utils.UserStorage import UserStorage
from utils.States import FindData
from keyboards.builders import num_kb
from keyboards import builders, inline
from filters.is_valid_date import IsValidDate
import phonenumbers
from aiogram.types import Message

from utils.extract_id import extract_id

router = Router()


@router.callback_query(FindData.enter_visit_date, F.data == "Назад")
async def enter_visit_date(callback: CallbackQuery, bot: Bot, state: FSMContext):
    profile = await get_profile(await extract_id(callback.message.caption))

    await bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        caption=profile[0],
        reply_markup=inline.context
    )
    await state.clear()
    await callback.answer()


@router.callback_query(FindData.enter_visit_date)
async def enter_visit_date(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[callback.from_user.id]
    profile = await get_profile(await extract_id(callback.message.caption))

    items = [
        "1", "2", "3",
        "4", "5", "6",
        "7", "8", "9",
        "0"
    ]

    for item in items:
        if len(user.temp) < 10 and item == callback.data:
            if len(user.temp) == 4 or len(user.temp) == 7:
                user.temp += "-"
            user.temp += callback.data

    if callback.data == "❌" and len(user.temp) >= 0:
        user.temp = user.temp[:-1]

    with suppress(TelegramBadRequest):
        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption=f"{profile[0]}"
                    f"      <pre>Дата: {user.temp}</pre>",
            reply_markup=builders.num_kb('find')
        )

    if callback.data == "OK" and len(user.temp) == 10:
        last_visit = await get_last_visit(await extract_id(callback.message.caption), user.temp)

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption=f"{profile[0] + last_visit[1] + last_visit[0]}",
            reply_markup=inline.context_unfold
        )
        await state.clear()

    await callback.answer()


@router.message(FindData.enter_visit_date, IsValidDate())
async def enter_visit_date(message: Message, bot: Bot, users: UserStorage, state: FSMContext):
    user = users.users_list[message.from_user.id]
    user.temp = message.text

    profile = await get_profile(user.temp_user_id)

    with suppress(TelegramBadRequest):
        await bot.edit_message_caption(
            chat_id=message.chat.id,
            caption=f"{profile[0]}"
                    f"      <pre>Дата: {user.temp}</pre>",
            message_id=user.temp_mess_id,
            reply_markup=num_kb()
        )
