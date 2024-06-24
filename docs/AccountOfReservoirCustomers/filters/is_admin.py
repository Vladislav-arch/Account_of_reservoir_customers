from __future__ import annotations

from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.UserStorage import UserStorage
from utils.Users import Users


class IsAdmin(BaseFilter):

    def __init__(self, user_ids: int | List[int]) -> None:
        self.user_ids = user_ids

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.user_ids, int):
            if message.from_user.id == self.user_ids or message.from_user.id in self.user_ids:
                if self.user_ids not in UserStorage.users_list:
                    UserStorage(user_id=message.from_user.id, obj=Users())
                    return True
                else:
                    return True


