from typing import Callable, Awaitable, Dict, Any

from cachetools import TTLCache
from aiogram.filters import BaseFilter
from aiogram.types import Message


class SavingIdMidleware(BaseFilter):
    def __init__(self, time_limit: int=4) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        print(2)

        if event.chat.id in self.limit:
            return
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data)