from __future__ import annotations

from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class PhoneNumIsCorrect(BaseFilter):
    async def __call__(self, message: Message, ) -> bool:
        if message.contact:
            return True
        else:
            await message.answer("Натисніть на кнопку!")




