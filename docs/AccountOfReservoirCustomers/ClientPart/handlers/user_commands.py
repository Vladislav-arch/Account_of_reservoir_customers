from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from twilio.rest import Client

#data
from ClientPart.data.check_from_user_id import check_from_user_id

#filters
from ClientPart.filters.from_user_id_collection import FromUserIdCollection

#utils
from ClientPart.utils.UserStorage import UserStorage

#keyboards
from ClientPart.keyboards import reply
from ClientPart.keyboards import builders

router = Router()


@router.message(CommandStart(), FromUserIdCollection())
async def start(mess: Message, bot: Bot, users: UserStorage):
    user = users.users_list[mess.from_user.id]

    await mess.answer(text=f"Вітаю {mess.from_user.first_name}!😊", reply_markup=reply.main)




