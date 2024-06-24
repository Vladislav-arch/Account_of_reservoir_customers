from __future__ import annotations

from datetime import datetime


from aiogram.filters import BaseFilter
from aiogram.types import Message


class VisitDateIsCorrect(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            datetime.strptime(message.text, '%Y-%m-%d')
            return True
        except ValueError:
            await message.answer("Введіть дату у форматі 'рік-місяць-день!")
            return False

