from __future__ import annotations

from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message

#utils
from ClientPart.utils.UserStorage import UserStorage
from ClientPart.utils.Users import Users


class FromUserIdCollection(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id not in UserStorage.users_list:
            UserStorage(user_id=message.from_user.id, obj=Users())
        return True


