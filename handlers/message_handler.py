from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from messages.message import MESSAGES
from buttons.button import start_menu, about_menu, connect_menu, cours_menu, back
from utils.states import Category, CheckStudent, Comment, Registration


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    mess = MESSAGES.get("start").get("text")
    for text in mess[0:-1]:
        await message.answer(f"{text}")
    await message.answer(f"{mess[-1]}", reply_markup=start_menu())


@dp.message_handler()
async def msg(message: types.Message, state: FSMContext):
    # user = message.chat
    user_msg = message.text
    if user_msg.lower() == "про нас":
        mess = MESSAGES.get("about_us").get("text")
        for text in mess[0:-1]:
            await message.answer(f"{text}")
        await message.answer(f"{mess[-1]}", reply_markup=about_menu())
    elif user_msg.lower() == "связаться с нами":
        mess = MESSAGES.get("connect").get("text")
        for text in mess[0:-1]:
            await message.answer(f"{text}")
        await message.answer(f"{mess[-1]}", reply_markup=connect_menu())
    elif user_msg.lower() == "наши контакты":
        mess = MESSAGES.get("contact").get("text")
        for text in mess:
            await message.answer(f"{text}")
        await message.answer_location(latitude=40.7600858, longitude=72.3490069)
    elif user_msg.lower() == "оставить заявку":
        await Registration.name.set()
        await message.answer("Введите своё имя", reply_markup=back())
    elif user_msg.lower() == "наши курсы":
        async with state.proxy() as data:
            data['to'] = "course"
        await Category.category.set()
        mess = MESSAGES.get("category").get("text")
        await message.answer(f"{mess[0]}", reply_markup=cours_menu())
    elif user_msg.lower() == "наша команда":
        async with state.proxy() as data:
            data['to'] = "teacher"
        await Category.category.set()
        mess = MESSAGES.get("category").get("text")
        await message.answer(f"{mess[0]}", reply_markup=cours_menu())
    elif user_msg.lower() == "цены":
        await message.answer_photo(open("./images/price.png", "rb"), caption="Цены")
    elif user_msg.lower() == "проверить задолженность":
        async with state.proxy() as data:
            data['to'] = "debt"
        await CheckStudent.name.set()
        await message.answer("Введите своё имя", reply_markup=back())
    elif user_msg.lower() == "узнать успеваемость студента":
        async with state.proxy() as data:
            data['to'] = "status"
        await CheckStudent.name.set()
        await message.answer("Введите своё имя", reply_markup=back())
    elif user_msg.lower() == "оставить отзыв":
        await Comment.name.set()
        await message.answer("Введите своё имя", reply_markup=back())
    elif user_msg.lower() == "🔙назад":
        mess = MESSAGES.get("start").get("text")
        await message.answer(f"{mess[-1]}", reply_markup=start_menu())
    else:
        mess = MESSAGES.get("start").get("text")
        await message.answer(f"{mess[-1]}", reply_markup=start_menu())
