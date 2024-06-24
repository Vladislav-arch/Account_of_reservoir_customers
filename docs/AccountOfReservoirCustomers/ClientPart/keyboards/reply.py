from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зареєструватись")],
        [KeyboardButton(text="Забронювати місце")],
        [KeyboardButton(text="Мій профіль")],
        #[KeyboardButton(text="Місця")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Вибери дію з меню"
)

contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поділитися своїм номером телефону", request_contact=True)],
        [KeyboardButton(text="Вийти")]
    ],
    resize_keyboard=True,

)

rmk = ReplyKeyboardRemove()