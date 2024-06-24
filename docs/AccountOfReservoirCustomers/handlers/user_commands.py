from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from filters.is_admin import IsAdmin
from utils.UserStorage import UserStorage
from data.db.get_profile import get_profile
from utils.check_datetime_passed import check_datetime_passed

from keyboards import reply
from data.subloader import get_json

router = Router()


@router.message(CommandStart(), IsAdmin(1266987522))
async def start(mess: Message, users: UserStorage, bot: Bot):
    print(mess.chat.id)
    await check_datetime_passed()
    await mess.answer(text=".", reply_markup=reply.main)



