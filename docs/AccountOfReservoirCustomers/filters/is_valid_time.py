from datetime import datetime
from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class ІsValidTime(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            datetime.strptime(message.text, '%H:%M')
            return True
        except ValueError:
            return False


