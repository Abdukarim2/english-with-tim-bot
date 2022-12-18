from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from messages.message import MESSAGES
from utils.db import get_course_category, get_hour, get_day, getall_teacher


def start_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    ms = MESSAGES.get("start").get("btn")
    for text in ms:
        kb.insert(
            KeyboardButton(f"{text}")
        )
    return kb


def about_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    ms = MESSAGES.get("about_us").get("btn")
    for text in ms:
        kb.insert(
            KeyboardButton(f"{text}")
        )
    return kb


def connect_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    ms = MESSAGES.get("connect").get("btn")
    for text in ms:
        kb.insert(
            KeyboardButton(f"{text}")
        )
    return kb


def cours_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for text in get_course_category():
        kb.insert(
            KeyboardButton(f"{text[0]}")
        )
    kb.insert(
        KeyboardButton("🔙Назад")
    )
    return kb


def back(one_time: bool = False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    kb.add(
        KeyboardButton("🔙Назад")
    )
    return kb


def back_send(one_time: bool = False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    kb.add(
        KeyboardButton("Отправить заявку"),
        KeyboardButton("🔙Назад")
    )
    return kb


def teacher():
    kb = InlineKeyboardMarkup(row_width=2)
    for item in getall_teacher():
        kb.insert(
            InlineKeyboardButton(item[0], callback_data=f"teacher_{item[0]}")
        )
    return kb


def hour():
    kb = InlineKeyboardMarkup(row_width=2)
    for item in get_hour():
        kb.insert(
            InlineKeyboardButton(item[1], callback_data=f"hour_{item[1]}")
        )
    kb.insert(
        InlineKeyboardButton("Вечерние", callback_data="hour_Вечерние")
    )
    return kb


def day():
    kb = InlineKeyboardMarkup(row_width=2)
    for item in get_day():
        kb.insert(
            InlineKeyboardButton(item[1], callback_data=f"day_{item[1]}")
        )
    return kb
