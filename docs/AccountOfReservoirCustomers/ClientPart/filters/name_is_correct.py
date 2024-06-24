from __future__ import annotations

from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class NameIsCorrect(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if 50 >= len(message.text) >= 3 >= len(message.text.split()) and bool(re.search(r'\d', message.text)) != True:
            return True
        elif message.text[:18] == "Використати ім`я: " and 66 >= len(message.text) >= 19 and 5 >= len(message.text.split()) and bool(re.search(r'\d', message.text)) != True:
            return True
        else:
            await message.answer("Ім`я не є коректним! Надайте інше!")
