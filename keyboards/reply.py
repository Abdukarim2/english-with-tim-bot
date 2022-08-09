from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def four_row(words: list, one_time: bool = False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        if one_time else ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text=words[0]),
        KeyboardButton(text=words[1])
    )
    markup.row(
        KeyboardButton(text=words[2]),
        KeyboardButton(text=words[3])
    )
    return markup


def three_row(words: list, one_time: bool = False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        if one_time else ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text=words[0]),
        KeyboardButton(text=words[1])
    )
    markup.add(
        KeyboardButton(text=words[2])
    )
    return markup


def remove():
    return ReplyKeyboardRemove()


def back(one_time: bool = False, additional: bool = False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        if one_time else ReplyKeyboardMarkup(resize_keyboard=True)
    if additional:
        markup.row(
            KeyboardButton(text="🧑‍💻Отправить заявку"),
            KeyboardButton(text="🔙Назад")
        )
    else:
        markup.add(
            KeyboardButton(text="🔙Назад")
        )
    return markup
