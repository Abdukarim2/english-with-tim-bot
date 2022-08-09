from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inlines(words: list, delete: str = None):
    markup = InlineKeyboardMarkup(row_width=2)
    action = ""
    if delete is not None:
        action = delete
    else:
        action = "teachers_"
    for i in words:
        markup.insert(
            InlineKeyboardButton(i[1], callback_data=f"{action}{i[1]}")
        )
    return markup
