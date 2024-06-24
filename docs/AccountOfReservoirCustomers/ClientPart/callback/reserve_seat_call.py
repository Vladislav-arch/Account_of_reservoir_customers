from datetime import date, timedelta, datetime

from aiogram import Router, F, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from contextlib import suppress
import asyncio
from data.db.table.static_information import insert_into_static_information

#utils
from ClientPart.utils.UserStorage import UserStorage
from ClientPart.utils.States import RegistrationClient, ReserveSeat
from utils.number_verification import number_verification
from ClientPart.utils.checking_reserved_seats import checking_reserved_seats

#keyboards
from ClientPart.keyboards import builders
from ClientPart.keyboards import reply

#data
from ClientPart.data.get_user import get_user

import phonenumbers

router = Router()


@router.callback_query(StateFilter(ReserveSeat.place, ReserveSeat.day, ReserveSeat.time), F.data.in_(["Вийти", ]))
async def reserve(callback: CallbackQuery, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[callback.from_user.id]

    if callback.data == "Вийти":
        with suppress(TelegramBadRequest):
            for u in user.mess_id_for_clean:
                await bot.delete_message(callback.message.chat.id, u)
            user.mess_id_for_clean = []
        await callback.message.answer("Бронювання скасовано!", reply_markup=reply.main)
        await state.clear()


@router.callback_query(ReserveSeat.place, F.data.in_(["Місце 1", "Місце 2", "Місце 3", "Місце 4", "Місце 5"]))
async def reserve(callback: CallbackQuery, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[callback.from_user.id]
    await state.update_data(place=callback.data)

    try:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=user.temp_mess_id)
    except TelegramBadRequest as e:
        print(e)

    photo = FSInputFile(f"photos/{callback.data}.jpg")

    if callback.data == "Місце 1":
        user.text = (
            "<pre>Місце 1 має глибокий берег, і тому воно підходить для ловлі на поплавок. Однак для дальнього забросу "
            "це місце не найкраще, оскільки тут багато кущів. 🎣</pre>"
            "<pre>Якщо ви бажаєте забронювати місце, оберіть дату, на яку ви хочете забронювати. Нижче відображаються "
            "лише вільні дати. 📅</pre>\n")
    elif callback.data == "Місце 2":
        user.text = (
            "<pre>Це місце ідеально підходить для ловлі на поплавок, оскільки має глибокий берег. Для дальнього забросу "
            "його можна використовувати, але не бажано, оскільки тут багато кущів. 🎣</pre>"
            "<pre>Якщо ви бажаєте забронювати місце, оберіть дату, на яку ви хочете забронювати. Нижче відображаються "
            "лише вільні дати. 📅</pre>\n")
    elif callback.data == "Місце 3":
        user.text = (
            "<pre>Це місце ідеально підходить для ловлі на поплавок, оскільки має глибокий берег. Для дальнього забросу "
            "його можна використовувати, але не бажано, оскільки тут багато кущів. 🎣</pre>"
            "<pre>Якщо ви бажаєте забронювати місце, оберіть дату, на яку ви хочете забронювати. Нижче відображаються "
            "лише вільні дати. 📅</pre>\n")
    elif callback.data == "Місце 4":
        user.text = (
            "<pre>Це місце є найулюбленішим серед людей, які люблять ловити на дальній заброс, оскільки тут чисте дно."
            " Воно також підходить для ловлі на поплавок, але порівняно з іншими місцями має мілке дно. 🎣🌊</pre>"
            "<pre>Якщо ви бажаєте забронювати місце, оберіть дату, на яку ви хочете забронювати. Нижче відображаються "
            "лише вільні дати. 📅</pre>\n")
    elif callback.data == "Місце 5":
        user.text = (
            "<pre>Місце схоже по характеристикам з міцем 4. Тут можна рибалити як на поплавок, так і на дальній заброс. 🎣🌊</pre>"
            "<pre>Якщо ви бажаєте забронювати місце, оберіть дату, на яку ви хочете забронювати. Нижче відображаються "
            "лише вільні дати. 📅</pre>\n")

    day = [f"{date.today()}", f"{date.today() + timedelta(days=1)}",
     f"{date.today() + timedelta(days=2)}",
     f"{date.today() + timedelta(days=3)}",
     f"{date.today() + timedelta(days=4)}",
     f"{date.today() + timedelta(days=5)}",
     f"{date.today() + timedelta(days=6)}", "Вийти"]
    free_days = []

    for d in day:
        if await checking_reserved_seats(callback.data, d):
            continue
        free_days.append(d)

    sent_mess = await callback.message.answer_photo(photo=photo, caption=user.text,
                                                    reply_markup=builders.day(free_days))
    user.temp_mess_id = sent_mess.message_id
    user.mess_id_for_clean.append(sent_mess.message_id)

    await callback.answer()


@router.callback_query(
    F.data.in_([f"{date.today()}", f"{date.today() + timedelta(days=1)}", f"{date.today() + timedelta(days=2)}",
                f"{date.today() + timedelta(days=3)}", f"{date.today() + timedelta(days=4)}",
                f"{date.today() + timedelta(days=5)}",
                f"{date.today() + timedelta(days=6)}"]))
async def reserve(callback: CallbackQuery, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[callback.from_user.id]
    await state.update_data(day=callback.data)

    mess = await bot.edit_message_caption(chat_id=callback.message.chat.id,
                                          message_id=user.temp_mess_id,
                                          caption=user.text + f"\nВведіть час на який бажаєте забронювати місце: {user.time}",
                                          reply_markup=builders.num_kb())
    user.mess_id_for_clean.append(mess.message_id)

    await state.set_state(ReserveSeat.time)


@router.callback_query(ReserveSeat.time)
async def reserve(callback: CallbackQuery, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[callback.from_user.id]

    if len(user.time) <= 4 and callback.data.isdigit():
        if len(user.time) == 2:
            user.time += ":"
        user.time += callback.data
    if callback.data == "❌":
        if len(user.time) == 4:
            user.time = user.time[:-1]
        user.time = user.time[:-1]
    if callback.data == "OK":
        data = await state.get_data()
        specified_date_str = f"{data['day']} {user.time}"
        current_date = datetime.now()
        try:
            specified_date = datetime.strptime(specified_date_str, '%Y-%m-%d %H:%M')
            if current_date > specified_date:
                await callback.answer("Вказаний час вже минув😠")
                return
            datetime.strptime(user.time, '%H:%M')
        except ValueError:
            await callback.answer("Введіть коректний час!😠")
            return

        await state.update_data(start_time=user.time)
        data = await get_user(callback.from_user.id)
        if data:
            await bot.edit_message_caption(chat_id=callback.message.chat.id,
                                           message_id=user.temp_mess_id,
                                           caption=user.text +
                                                   f"Залишити ці дані?🤔"
                                                   f"<pre>Ім`я: {data[1]}</pre><pre>Телефон: {data[2]}</pre>",
                                           reply_markup=builders.profile_inline(["Так", "Ні. Я надам інші дані"]))
            await state.set_state(ReserveSeat.choice)
        else:
            await callback.message.answer("Надайте своє ім`я",
                                          reply_markup=builders.profile11(
                                              [f"Використати ім`я: {callback.from_user.first_name}", "Вийти"]))
            await state.set_state(ReserveSeat.name)

        return

    with suppress(TelegramBadRequest):
        mess = await bot.edit_message_caption(chat_id=callback.message.chat.id,
                                              message_id=user.temp_mess_id,
                                              caption=user.text + f"\nВведіть час на який бажаєте забронювати місце: <b>{user.time}</b>",
                                              reply_markup=builders.num_kb())
        user.mess_id_for_clean.append(mess.message_id)
    await callback.answer()


@router.callback_query(ReserveSeat.choice)
async def reserve(callback: CallbackQuery, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[callback.from_user.id]

    if callback.data == "Так":
        data = await get_user(callback.from_user.id)
        await state.update_data(user_phone=data[2], name=data[1])
        await callback.message.answer("Надайте передплату за місце💸", reply_markup=builders.profile("Вийти"))
        mess = await bot.send_invoice(callback.message.chat.id,
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
    elif callback.data == "Ні. Я надам інші дані":
        await callback.message.answer("Надайте своє ім`я",
                                      reply_markup=builders.profile11(
                                          [f"Використати ім`я: {callback.from_user.first_name}", "Вийти"]))
        await state.set_state(ReserveSeat.name)


@router.callback_query(F.data.in_(["Впевнений", "Не буду бронювати"]))
async def reserve(callback: CallbackQuery, state: FSMContext, users: UserStorage, bot: Bot):
    user = users.users_list[callback.from_user.id]

    if callback.data == "Впевнений":
        mess = await callback.message.answer(".", reply_markup=reply.rmk)
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=mess.message_id)
        await callback.message.answer("Добре! Яке ви бажаєте обрати місце для риболовлі?🤔",
                                      reply_markup=builders.places(
                                          ["Місце 1", "Місце 2", "Місце 3", "Місце 4", "Місце 5", "Вийти"]))
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await state.set_state(ReserveSeat.place)
    elif callback.data == "Не буду бронювати":
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await callback.message.answer("Вас зрозумів!")
        await state.clear()
