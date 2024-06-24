from aiogram import Router, F, Bot, types
from aiogram.types import Message
from data.db.get_ids import get_ids
from data.db.get_profile import get_profile
from keyboards import inline
from aiogram.fsm.context import FSMContext
from utils.States import Pagination_profile
from filters.phone_num_is_correct import PhoneNumIsCorrect
from filters.name_is_correct import NameIsCorrect
from keyboards import fabrics
from utils.Users import Users
from utils.UserStorage import UserStorage
from data.db.update_data import update_data
from data.db.get_profile import get_profile
from keyboards.fabrics import Pagination

router = Router()


@router.message(Pagination_profile.editing_profiles, F.photo)
async def edit_photo(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]

    await update_data("static_information", "photo", message.photo[-1].file_id, id=user.profile_id)

    mess_id = user.temp_mess_id
    caption = await get_profile(user.profile_id)
    new_photo = types.InputMediaPhoto(media=message.photo[-1].file_id,
                                      caption=caption[0])

    await bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=mess_id,
        media=new_photo,
        reply_markup=inline.context
    )
    await state.clear()


@router.message(Pagination_profile.editing_profiles, PhoneNumIsCorrect())
async def edit_phone_num(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    id = user.profile_id
    mess_id = user.temp_mess_id

    await update_data("static_information", "phone_num", f"+380{message.text}", id)
    caption = await get_profile(id)

    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=mess_id,
        caption=caption[0],
        reply_markup=inline.context
    )
    await state.clear()


@router.message(Pagination_profile.editing_profiles, NameIsCorrect())
async def edit_phone_num(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]
    id = user.profile_id
    mess_id = user.temp_mess_id

    await update_data("static_information", "name", message.text, id)
    caption = await get_profile(id)

    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=mess_id,
        caption=caption[0],
        reply_markup=inline.context
    )
    await state.clear()


@router.message(Pagination_profile.editing_profiles)
async def data_is_correct(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    await message.answer("Дані не є коректними!")
