from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    phone_num = State()
    photo = State()

    #continue_or_stop = State()

    deff = State()

    user_id = State()
    visit_date = State()
    fishing_place = State()
    tariff = State()


class Pagination_profile(StatesGroup):
    editing_profiles = State()


class SearchCustomer(StatesGroup):
    search = State()


class RegistrationFish(StatesGroup):
    fish_weight = State()
    trophy_fish = State()
    photo_of_trophy_fish = State()


class FindData(StatesGroup):
    enter_visit_date = State()


class ReserveSeat(StatesGroup):
    day = State()
    place = State()

    reserve_seat = State()

    start_time = State()

    user_phone = State()


class Photo(StatesGroup):
    choose_place = State()
    set_photo = State()


class DeleteReserve(StatesGroup):
    data_to_delete = State()
    yes_or_no = State()