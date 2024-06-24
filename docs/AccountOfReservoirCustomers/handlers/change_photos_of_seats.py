import os

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from data.db.get_ids import get_ids
from data.db.get_profile import get_profile
from keyboards import inline, reply
from aiogram.fsm.context import FSMContext
from utils.States import Pagination_profile, Photo
from filters.phone_num_is_correct import PhoneNumIsCorrect
from filters.name_is_correct import NameIsCorrect
from keyboards import fabrics
from utils.Users import Users
from utils.UserStorage import UserStorage
from data.db.update_data import update_data
from data.db.get_profile import get_profile
from keyboards import builders
from data.db.table.photos import insert_photos


router = Router()


@router.message(StateFilter(Photo.choose_place, Photo.set_photo),F.text == "Назад")
async def change_photo(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    await message.answer("Операцію скасовано!",
                         reply_markup=reply.main)
    await state.clear()


@router.message(F.text == "Змінити фото місць")
async def change_photo(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]

    await message.answer("Оберіть місце для встановлення фото",
                         reply_markup=builders.places(["Місце 1", "Місце 2", "Місце 3", "Місце 4", "Місце 5", "Назад"])
    )
    await state.set_state(Photo.choose_place)


@router.message(Photo.choose_place, F.text.in_(["Місце 1", "Місце 2", "Місце 3", "Місце 5", "Місце 4"]))
async def change_photo(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]

    await state.update_data(place=message.text)

    await message.answer("Надайте фото")
    await state.set_state(Photo.set_photo)


@router.message(Photo.set_photo)
async def change_photo(message: Message, state: FSMContext, bot: Bot, users: UserStorage):
    user = users.users_list[message.from_user.id]

    data = await state.get_data()

    if os.path.exists(f'photos/{data['place']}.jpg'):
        os.remove(f'photos/{data['place']}.jpg')

    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f'photos/{data['place']}.jpg')
    print(f"Завантажено фото: {file_path}")

    await message.answer("Готово! Фото зміненою.",
                         reply_markup=reply.main)
    await state.clear()



