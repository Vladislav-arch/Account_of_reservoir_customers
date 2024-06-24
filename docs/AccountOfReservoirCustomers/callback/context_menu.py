from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from data.db.delete_customer import delete_customer
from utils.extract_id import extract_id
from utils.UserStorage import UserStorage
from contextlib import suppress
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from data.db.get_profile import get_profile
from keyboards import inline
from utils.wrap_in_pre_tag import wrap_in_pre_tag
from keyboards import builders
from data.db.get_last_visit import get_last_visit
from utils.States import Pagination_profile, Registration, FindData, RegistrationFish
from datetime import date, timedelta, datetime
from utils.extract_date import extract_date
from data.db.get_result_of_the_last_visit import get_result_of_the_last_visit
import phonenumbers

router = Router()


@router.callback_query(F.data.in_(['delete_profile', 'Так', 'Ні']))
async def delete_profile(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    caption = await get_profile(await extract_id(callback.message.caption))
    caption = await wrap_in_pre_tag(caption[0])

    if callback.data == "Так":
        await delete_customer(await extract_id(callback.message.caption))
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    elif callback.data == "delete_profile":
        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption=caption,
            reply_markup=builders.profile_inline(["Так", "Ні"])
        )
    elif callback.data == "Ні":
        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption=caption,
            reply_markup=inline.context
        )


@router.callback_query(F.data == "edit_profile")
async def edit_profile(callback: CallbackQuery, bot: Bot, users: UserStorage, state: FSMContext):
    users.users_list[callback.from_user.id].profile_id = await extract_id(callback.message.caption)
    users.users_list[callback.from_user.id].temp_mess_id = callback.message.message_id

    caption = await get_profile(await extract_id(callback.message.caption))

    mess = await bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        caption=caption[0],
        reply_markup=inline.edit_profile
    )
    await callback.answer("Режим редагування вмик.")
    await state.set_state(Pagination_profile.editing_profiles)


@router.callback_query(F.data == "unfold")
async def unfold_profile(callback: CallbackQuery, bot: Bot):
    profile = await get_profile(await extract_id(callback.message.caption))
    last_visit = await get_last_visit(await extract_id(callback.message.caption))

    await bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        caption=f"{profile[0] + last_visit[1] + last_visit[0]}",
        reply_markup=inline.context_unfold
    )


@router.callback_query(F.data == "hide")
async def hide_profile(callback: CallbackQuery, bot: Bot):
    profile = await get_profile(await extract_id(callback.message.caption))

    await bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        caption=profile[0],
        reply_markup=inline.context
    )


@router.callback_query(Pagination_profile.editing_profiles, F.data == "back")
async def pagination_back_handler(callback: CallbackQuery, bot: Bot, state: FSMContext, users: UserStorage):
    data = await get_profile(await extract_id(callback.message.caption))

    await bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        caption=data[0],
        reply_markup=inline.context

    )
    await state.clear()
    await callback.answer("Режим редагування вимк.")


@router.callback_query(F.data == "add_visit")
async def add_visit(callback: CallbackQuery, bot: Bot, state: FSMContext, users: UserStorage):
    user = users.users_list[callback.from_user.id]

    await state.set_state(Registration.visit_date)
    await state.update_data(user_id=await extract_id(callback.message.caption))

    sent_mess = await bot.send_message(
        chat_id=callback.message.chat.id,
        text="Надайте дату відвідування: ",
        reply_markup=builders.profile([f"{date.today()}", f"{date.today() - timedelta(days=1)}", "Назад"])
    )
    user.id_for_secondary_cleaning.append(sent_mess.message_id)


@router.callback_query(F.data == "add_result_of_the_visit")
async def result_of_the_visit(callback: CallbackQuery, bot: Bot, state: FSMContext, users: UserStorage):
    user = users.users_list[callback.from_user.id]
    if await get_result_of_the_last_visit(await extract_id(callback.message.caption), await extract_date(callback.message.caption)):
        await callback.answer("До даного відвідування уже є результат!")
        return

    await state.update_data(visit_date=await extract_date(callback.message.caption))
    await state.update_data(user_id=await extract_id(callback.message.caption))

    await state.set_state(RegistrationFish.fish_weight)
    mess = await callback.message.answer("Вкажіть вагу риби: ", reply_markup=builders.profile("Назад"))
    user.id_for_secondary_cleaning.append(mess.message_id)
    await callback.answer()


@router.callback_query(F.data == "result_of_the_visit")
async def add_visit(callback: CallbackQuery, bot: Bot, state: FSMContext, users: UserStorage):
    user = users.users_list[callback.from_user.id]

    id = await extract_id(callback.message.caption)
    date = await extract_date(callback.message.caption)
    print(date)

    data = await get_result_of_the_last_visit(id, date)

    if data:
        if data[0]:
            mess = await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=data[0],
                caption=data[1],
            )
            user.id_for_full_cleanup.append(mess.message_id)
        else:
            mess = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=data[1],
            )
            user.id_for_full_cleanup.append(mess.message_id)
    else:
        await callback.answer("Дані відсутні")


@router.callback_query(F.data == "find_visit")
async def find_visit(callback: CallbackQuery, bot: Bot, state: FSMContext, users: UserStorage):
    await state.set_state(FindData.enter_visit_date)

    user = users.users_list[callback.from_user.id]
    user.temp_mess_id = callback.message.message_id
    user.temp_user_id = await extract_id(callback.message.caption)
    now = datetime.now()
    month = now.strftime("%m")
    user.temp = f"{now.year}-{month}"

    profile = await get_profile(await extract_id(callback.message.caption))

    await bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        caption=f"{profile[0]}"
                f"      <pre>Дата: {user.temp}</pre>",
        reply_markup=builders.num_kb('find')
    )