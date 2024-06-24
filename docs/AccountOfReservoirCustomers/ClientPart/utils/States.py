from aiogram.fsm.state import State, StatesGroup


class RegistrationClient(StatesGroup):
    name = State()
    phone_num = State()

    phone_number_confirmation = State()


class ReserveSeat(StatesGroup):
    place = State()
    day = State()
    time = State()

    choice = State()

    user_phone = State()
    name = State()

    pay = State()


class Profile(StatesGroup):
    profile = State()

    edit_profile = State()

    name = State()
    phone = State()

