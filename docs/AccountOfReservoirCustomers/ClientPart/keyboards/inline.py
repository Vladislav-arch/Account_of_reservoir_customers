from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="YouTube"),
            InlineKeyboardButton(text="Telegram")
        ]
    ]
)

context = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔽", callback_data="unfold"),
        ],
[
            InlineKeyboardButton(text="Додати відвідування", callback_data="add_visit"),
            InlineKeyboardButton(text="Знайти відвідування", callback_data="find_visit"),
        ],
        [
            InlineKeyboardButton(text="✏️", callback_data="edit_profile"),
            InlineKeyboardButton(text="❌", callback_data="delete_profile")
        ]
    ]
)

edit_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙", callback_data="back"),
        ],
    ]
)

context_unfold = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔼", callback_data="hide"),
        ],
        [
            InlineKeyboardButton(text="Додати результат відвідування", callback_data="add_result_of_the_visit"),
            InlineKeyboardButton(text="Результат відвідування", callback_data="result_of_the_visit"),

        ],
    ]
)