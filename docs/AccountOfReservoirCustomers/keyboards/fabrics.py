from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def paginator(page: int = 1):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔼", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text="🔽", callback_data=Pagination(action="next", page=page).pack()),
        InlineKeyboardButton(text="🔙", callback_data=Pagination(action="back", page=page).pack()),
        width=2
    )
    return builder.as_markup()

