from __future__ import annotations

from datetime import datetime
from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class IsValidDate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            datetime.strptime(message.text, '%Y-%m-%d')
            return True
        except ValueError:
            await message.answer("Дата не коректна!")
            return False
