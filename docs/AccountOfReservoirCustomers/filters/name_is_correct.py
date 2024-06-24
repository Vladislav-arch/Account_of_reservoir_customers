from __future__ import annotations

from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class NameIsCorrect(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if 50 >= len(message.text) >= 3 >= len(message.text.split()) and bool(re.search(r'\d', message.text)) != True:
            return True
