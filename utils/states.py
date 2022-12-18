from aiogram.dispatcher.filters.state import State, StatesGroup


class Category(StatesGroup):
    category = State()


class CheckStudent(StatesGroup):
    name = State()
    surname = State()
    teacher = State()
    date = State()
    days = State()
    number = State()


class Comment(StatesGroup):
    name = State()
    surname = State()
    number = State()
    comment = State()
    

class Registration(StatesGroup):
    name = State()
    surname = State()
    number1 = State()
    number2 = State()
    course = State()
    comment = State()
