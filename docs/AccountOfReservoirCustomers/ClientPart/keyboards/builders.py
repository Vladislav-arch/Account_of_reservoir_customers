from __future__ import annotations
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def num_kb():
    items = [
        "1", "2", "3",
        "4", "5", "6",
        "7", "8", "9",
        "0", "❌", "OK",
        "Вийти"
    ]

    builder = InlineKeyboardBuilder()

    [builder.button(text=f"{item}", callback_data=f"{item}") for item in items]

    builder.adjust(3, 3, 3, 3)

    return builder.as_markup(resize_keyboard=True)


def profile11(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt, callback_data=txt) for txt in text]
    builder.adjust(1, 1)

    return builder.as_markup(resize_keyboard=True)


def profile_inline11(text: str | list):
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt, callback_data=txt) for txt in text]
    builder.adjust(1, 1)

    return builder.as_markup(resize_keyboard=True)


def profile(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt, callback_data=txt) for txt in text]
    builder.adjust(2, 2)

    return builder.as_markup(resize_keyboard=True)


def profile_inline(text: str | list):
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt, callback_data=txt) for txt in text]
    builder.adjust(2, 2)

    return builder.as_markup(resize_keyboard=True)


def places(text: str | list):
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt, callback_data=txt) for txt in text]
    builder.adjust(3, 2, 1)

    return builder.as_markup(resize_keyboard=True)


def day(text: str | list):
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt, callback_data=txt) for txt in text]
    builder.adjust(3, 2, 2, 1)

    return builder.as_markup(resize_keyboard=True)