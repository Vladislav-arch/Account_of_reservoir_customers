import asyncio
from contextlib import suppress
from datetime import date, timedelta

from aiogram import Router, F, Bot, types
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import Message, Contact, FSInputFile, successful_payment
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Contact, pre_checkout_query
from aiogram.types import InputFile

from ClientPart.data.check_from_user_id import check_from_user_id
# keyboard
from ClientPart.keyboards import builders
from ClientPart.keyboards import reply

# filters
from ClientPart.filters.name_is_correct import NameIsCorrect
from ClientPart.filters.phone_num_is_correct import PhoneNumIsCorrect

# utils
from ClientPart.utils.UserStorage import UserStorage
from ClientPart.utils.States import RegistrationClient, ReserveSeat
from ClientPart.utils.checker import checker
from utils.Places import Places

# data
from data.db.table.static_information import insert_into_static_information
from ClientPart.data.get_user import get_user

from utils.number_verification import number_verification

router = Router()


@router.message(StateFilter(ReserveSeat.name, ReserveSeat.pay), F.text == "Вийти")
async def reserve(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]

    if message.text == "Вийти":
        for u in user.mess_id_for_clean:
            with suppress(TelegramBadRequest):
                await bot.delete_message(message.chat.id, u)
        user.mess_id_for_clean = []
        await message.answer("Бронювання скасовано!", reply_markup=reply.main)
        await state.clear()


@router.message(F.text == "Забронювати місце")
async def reserve(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    data = await get_user(message.from_user.id)

    if data:
        if await checker(data[2], "user_phone", table="reserved_seats"):
            await message.answer("Ви вже маєте бронювання. Ви впевнені що хочете забронювати ще?🤨",
                                 reply_markup=builders.profile_inline(["Впевнений", "Не буду бронювати"]))
            return
    mess = await message.answer(".", reply_markup=reply.rmk)
    await bot.delete_message(chat_id=message.chat.id, message_id=mess.message_id)
    mess = await message.answer("Яке ви бажаєте обрати місце для риболовлі?🤔",
                                reply_markup=builders.places(
                                    ["Місце 1", "Місце 2", "Місце 3", "Місце 4", "Місце 5", "Вийти"]))
    user.mess_id_for_clean.append(mess.message_id)

    await state.set_state(ReserveSeat.place)


@router.message(ReserveSeat.time)
async def reserve(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]

    data = await get_user(message.from_user.id)

    if await checker(message.from_user.id, "from_user_id"):
        await message.answer(f"Використати ці дані?"
                             f"<pre>Телефон: {data[2]}</pre>"
                             f"<pre>Ім`я: {data[1]}</pre>",
                             reply_markup=builders.profile(["Так", "Ні. Я надам сам"]))
    await state.set_state(ReserveSeat.pay)


@router.pre_checkout_query(ReserveSeat.pay, lambda query: True)
async def process_pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if await checker(column="place", data=data['place'], column2="day", data2=data['day'], table="reserved_seats2"):
        await pre_checkout_q.answer(
            ok=False,
            error_message="Схоже це місце хтось уже забронював. Спробуйте заново😢"
        )
        return
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(ReserveSeat.pay, F.successful_payment)
async def reserve(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    p = Places(message.chat.id, bot)

    data = await state.get_data()

    await p.reserve_a_seat(data)
    asyncio.create_task(p.delete_automatically(data, client=True))

    for u in user.mess_id_for_clean:
        with suppress(TelegramBadRequest):
            await bot.delete_message(message.chat.id, u)
    user.mess_id_for_clean = []
    await state.clear()
    await message.answer(
        f"Готово! Місце заброньоване!🎉\nДякуємо за оплату!😊 Чекаємо вас <b>{data['day']}</b> о <b>{data['start_time']}</b> у нас на ставку!",
        reply_markup=reply.main)

    if not await check_from_user_id(message.from_user.id):
        await message.answer("Рекомендую вам зареєстуватись, так ви зможете бронювати місця ще швидше. Бажаєте "
                             "зареєструватись?😏",
                             reply_markup=builders.profile_inline(["Бажаю", "Потім"]))


@router.message(ReserveSeat.name)
async def form_name(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]

    if message.text[:18] == "Використати ім`я: ":
        name = message.text[18:]
    else:
        name = message.text

    await state.update_data(name=name)
    await state.set_state(ReserveSeat.user_phone)

    await message.answer("Надайте номер телефону",
                         reply_markup=reply.contact)


@router.message(ReserveSeat.user_phone, PhoneNumIsCorrect())
async def form_phone_num(message: Message, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[message.from_user.id]
    contact: Contact = message.contact

    if contact.phone_number:
        phone_number = contact.phone_number
        if phone_number[0] != "+":
            phone_number = '+' + contact.phone_number

    await state.update_data(user_phone=phone_number)
    await message.answer("Надайте передплату за місце💸", reply_markup=builders.profile("Вийти"))
    mess = await bot.send_invoice(message.chat.id,
                                  title="Передплату за місце",
                                  description="Місце 1",
                                  provider_token="410694247:TEST:78a56796-75c8-433e-b614-5b09b365e44e",
                                  currency="UAH",
                                  photo_url="https://tech.24tv.ua/resources/photos/news/202206/2041219.jpg?v=1661253043000&q=100",
                                  photo_width=416,
                                  photo_height=234,
                                  photo_size=416,
                                  is_flexible=False,
                                  prices=[types.LabeledPrice(label="Предоплата за місце", amount=100 * 100)],
                                  start_parameter="fdsffddsf",
                                  payload="test-invoice-pyload"
                                  )
    user.mess_id_for_clean.append(mess.message_id)
    await state.set_state(ReserveSeat.pay)
