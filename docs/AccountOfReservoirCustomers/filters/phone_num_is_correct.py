from __future__ import annotations

from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class PhoneNumIsCorrect(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if 9 == len(message.text) and message.text.isdigit():
            print(message.text)
            return True

