from aiogram.filters.state import State, StatesGroup


class ReminderStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_date = State()
    waiting_for_message = State()
