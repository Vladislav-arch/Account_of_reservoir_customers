import asyncio
from contextlib import suppress

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.States import Registration, RegistrationFish, ReserveSeat
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
from utils.chat_cleaning import chat_cleaning
from utils.Reminder import Reminder
from utils.check_date import check_date

router = Router()


@router.message(F.text == "Зареєструвати")
async def fill_profile(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)
    await chat_cleaning(user, bot, message.chat.id, user.id_for_full_cleanup)
    sent_mess = await message.answer("Зареєструвати", reply_markup=reply.main)
    user.id_for_full_cleanup.append(sent_mess.message_id)

    await state.set_state(Registration.name)
    await state.update_data(id=None)
    sent_mess = await message.answer(text="Надайте ім'я: ", reply_markup=builders.profile("Назад"))
    user.id_for_full_cleanup.append(sent_mess.message_id)


@router.message(StateFilter(Registration.name, Registration.phone_num, Registration.photo, Registration.visit_date,
                            Registration.tariff, Registration.fishing_place), F.text == "Назад")
async def form_back(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)

    await state.clear()

    await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, user.id_for_full_cleanup))

    sent_mess = await message.answer(
        "Операцію скасовано!",
        reply_markup=reply.main
    )
    user.id_for_full_cleanup.append(sent_mess.message_id)


@router.message(Registration.name, NameIsCorrect())
async def form_name(message: Message, state: FSMContext, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)

    await state.update_data(name=message.text)
    await state.set_state(Registration.phone_num)

    sents_mess = await message.answer(
        f"Надайте номер телефону: {user.phone_number}",
        reply_markup=num_kb()
    )
    user.temp_mess_id = sents_mess.message_id
    user.id_for_full_cleanup.append(sents_mess.message_id)


@router.message(StateFilter(Registration.phone_num, ReserveSeat.user_phone), PhoneNumIsCorrect())
async def form_phone_num(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)
    user.phone_number = "+380" + message.text

    with suppress(TelegramBadRequest):
        sent_mess = await bot.edit_message_text(
            chat_id=message.chat.id,
            text=f"Надайте номер телефону: {user.phone_number}",
            message_id=user.temp_mess_id,
            reply_markup=num_kb()
        )
        user.id_for_full_cleanup.append(sent_mess.message_id)


@router.message(Registration.photo, F.photo)
async def form_photo(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_full_cleanup.append(message.message_id)

    await state.update_data(photo=message.photo[-1].file_id)
    await state.update_data(from_user_id=None)
    await insert_into_static_information(await state.get_data())
    await state.clear()

    sent_mess = await message.answer(
       "Реєстрація завершена!",
       reply_markup=reply.main
    )
    user.id_for_full_cleanup.append(sent_mess.message_id)


@router.message(Registration.photo, ~F.photo)
async def incorrect_form_photo(message: Message, users: UserStorage):
    user = users.users_list[message.from_user.id]

    sent_mess = await message.answer("Надайте фото!")
    user.id_for_full_cleanup.append(sent_mess.message_id)

#-------------------------------------------------------


#@router.message(Registration.continue_or_stop, F.text.casefold().in_(["завершити", "продовжити"]))
#async def continue_or_stop(message: Message, state: FSMContext):
#    await insert_into_static_information(await state.get_data())
#    if message.text == "Завершити":
#        await state.clear()
#        await message.answer("Реєстрація завершена!", reply_markup=reply.main)
#    elif message.text == "Продовжити":
#        await state.set_state(Registration.visit_date)
#        await message.answer(
#            "Надайте дату відвідування: ",
#            reply_markup=builders.profile([f"{date.today()}", f"{date.today() - timedelta(days=1)}"])
#        )
#    else:
#        await message.answer("Натисніть на кнопку!")


@router.message(Registration.visit_date, VisitDateIsCorrect())
async def form_visit_date(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    user.id_for_secondary_cleaning.append(message.message_id)

    if await check_date(message.text):
        sent_mess = await message.answer("Відвідування з даною датою уже зареєстроване. Надайте іншу дат.")
        await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, [sent_mess.message_id, message.message_id], 3))
        return

    await state.update_data(visit_date=message.text)
    await state.set_state(Registration.fishing_place)

    sent_mess = await message.answer(
        "Вкажіть місце ловлі: ",
        reply_markup=builders.profile(["Місце 1", "Місце 2", "Місце 3", "Місце 4", "Назад"])
    )
    user.id_for_secondary_cleaning.append(sent_mess.message_id)


@router.message(Registration.fishing_place, F.text.casefold().in_(["місце 1", "місце 2", "місце 3", "місце 4"]))
async def form_place(message: Message, state: FSMContext, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_secondary_cleaning.append(message.message_id)

    await state.update_data(fishing_place=message.text)
    await state.set_state(Registration.tariff)

    sent_mess = await message.answer(
        "Вкажіть тариф: ",
        reply_markup=builders.profile(["День", "Сутки", "Назад"])
    )
    user.id_for_secondary_cleaning.append(sent_mess.message_id)


@router.message(Registration.tariff, F.text.casefold().in_(["день", "сутки"]))
async def form_tariff(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    user.id_for_secondary_cleaning.append(message.message_id)

    await state.update_data(tariff=message.text)
    data = await state.get_data()
    await insert_into_dynamic_information(data)

    reminder = Reminder(message.text, message.chat.id, bot, data['user_id'])
    asyncio.create_task(reminder.validity_period_ticket())

    await state.clear()
    sent_mess = await message.answer("Готово!", reply_markup=reply.main)
    user.id_for_full_cleanup.append(sent_mess.message_id)

    await asyncio.create_task(chat_cleaning(user, bot, message.chat.id, user.id_for_secondary_cleaning, 4))



