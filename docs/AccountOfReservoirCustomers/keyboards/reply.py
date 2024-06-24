from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зареєструвати")],
        [KeyboardButton(text="Клієнти"), KeyboardButton(text="Клієнти за сьогодні")],
        [KeyboardButton(text="Пошук")],
        [KeyboardButton(text="Місця"), KeyboardButton(text="Змінити фото місць")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Вибери дію з меню"
)

maain = ReplyKeyboardMarkup(
   keyboard=[
        [
            KeyboardButton(text="Смайлики"),
            KeyboardButton(text="Посилання")
        ],
        [
            KeyboardButton(text="Калькулятор"),
            KeyboardButton(text="Доп. кнопки")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Вибери дію з меню"
)

spec = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Відправити гео", request_location=True),
            KeyboardButton(text="Відправити контакт", request_contact=True),
            KeyboardButton(text="Відправити контакт", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text="НАЗАД")
        ]
    ]
)


rmk = ReplyKeyboardRemove()#