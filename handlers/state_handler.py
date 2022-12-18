from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.states import Category, CheckStudent, Comment, Registration
from loader import dp, bot
from messages.message import MESSAGES
from buttons.button import about_menu, cours_menu, connect_menu, teacher, hour, day, back_send, start_menu
from utils.db import get_course, get_teacher, get_course_category, create_student
from configs.config import GROUP_ID


@dp.message_handler(state=Category.category)
async def category(message: types.Message, state: FSMContext):
    user_msg = message.text
    courses = get_course(user_msg.lower())
    teachers = get_teacher(user_msg.lower())
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            mess = MESSAGES.get("about_us").get("text")
            await message.answer(f"{mess[-1]}", reply_markup=about_menu())
        elif courses and data.get("to") == "course":
            for course in courses:
                await message.answer(f"<b>{course[1]}</b>\n{course[2]}")
        elif teachers and data.get("to") == "teacher":
            for teacher in teachers:
                await message.answer(f"<b>{teacher[1]}</b>\n{teacher[2]}")
        else:
            mess = MESSAGES.get("category").get("text")
            await message.answer(f"{mess[0]}", reply_markup=cours_menu())


@dp.message_handler(state=CheckStudent.name)
async def check_st_name(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=connect_menu())
        else:
            if len(user_msg.lower()) >= 3 and user_msg.isalpha():
                data['name'] = user_msg
                await CheckStudent.next()
                await message.answer("Введите свою фамилию")
            else:
                await message.answer("Введите правильно")


@dp.message_handler(state=CheckStudent.surname)
async def check_st_surname(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=connect_menu())
        else:
            if len(user_msg.lower()) >= 3 and user_msg.isalpha():
                data['surname'] = user_msg
                await CheckStudent.next()
                await message.answer("У кого вы учитесь?\nВыберите имя учителя", reply_markup=teacher())
            else:
                await message.answer("Введите правильно")


@dp.message_handler(state=CheckStudent.teacher)
async def check_st_teacher(message: types.Message, state: FSMContext):
    user_msg = message.text
    if user_msg.lower() == "🔙назад":
        await state.finish()
        await message.answer(f"Выберите категорию", reply_markup=connect_menu())
    else:
        await message.answer("У кого вы учитесь?\nВыберите имя учителя", reply_markup=teacher())


@dp.callback_query_handler(lambda call: True, state=CheckStudent.teacher)
async def check_st_teacher_call(message: types.CallbackQuery, state: FSMContext):
    teacher_name = message.data[8:]
    async with state.proxy() as data:
        data['teacher'] = teacher_name
        await CheckStudent.next()
        await bot.edit_message_text("Во сколько начинаются ваши уроки?", message.from_user.id, message.message.message_id, reply_markup=hour())


@dp.message_handler(state=CheckStudent.date)
async def check_st_hour(message: types.Message, state: FSMContext):
    user_msg = message.text
    if user_msg.lower() == "🔙назад":
        await state.finish()
        await message.answer(f"Выберите категорию", reply_markup=connect_menu())
    else:
        await message.answer("Во сколько начинаются ваши уроки?", reply_markup=hour())


@dp.callback_query_handler(lambda call: True, state=CheckStudent.date)
async def check_st_hour_call(message: types.CallbackQuery, state: FSMContext):
    st_hour = message.data[5:]
    async with state.proxy() as data:
        data['hour'] = st_hour
        await CheckStudent.next()
        await bot.edit_message_text("В какие дни вы приходите на курсы?", message.from_user.id, message.message.message_id, reply_markup=day())


@dp.message_handler(state=CheckStudent.days)
async def check_st_day(message: types.Message, state: FSMContext):
    user_msg = message.text
    if user_msg.lower() == "🔙назад":
        await state.finish()
        await message.answer(f"Выберите категорию", reply_markup=connect_menu())
    else:
        await message.answer("В какие дни вы приходите на курсы?", reply_markup=day())


@dp.callback_query_handler(lambda call: True, state=CheckStudent.days)
async def check_st_day_call(message: types.CallbackQuery, state: FSMContext):
    st_days = message.data[4:]
    async with state.proxy() as data:
        data['days'] = st_days
        await CheckStudent.next()
        await bot.edit_message_text("Введите ваш номер телефона", message.from_user.id, message.message.message_id)


@dp.message_handler(state=CheckStudent.number)
async def check_st_number(message: types.Message, state: FSMContext):
    user_msg = message.text
    username = message.chat.username
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=connect_menu())
        else:
            if user_msg.strip("+").isdigit() and len(user_msg.strip("+")) == 9 or len(user_msg.strip("+")) == 12 and "." not in user_msg.strip("+"):
                data['number'] = user_msg
                await message.answer("Ваш запрос успешно отправлен. Мы скоро с вами свяжемся", reply_markup=connect_menu())
                await state.finish()
                data_dict = data.as_dict()
                if data_dict.get("to") == "status":
                    message_to_gr = f"<b>Davomadni tekshirish</b>\n\n<b>Ismi</b>\n{data_dict.get('name')}\n\n<b>Familyasi</b>\n{data_dict.get('surname')}\n\n<b>O'qituvchisi</b>\n{data_dict.get('teacher')}\n\n<b>Dars soati</b>\n{data_dict.get('hour')}\n\n<b>Dars kunlari</b>\n{data_dict.get('days')}\n\n<b>Telefo'n raqami</b>\n{data_dict.get('number')}"
                    if username:
                        message_to_gr = f"<b>Davomadni tekshirish</b>\n\n<b>Ismi</b>\n{data_dict.get('name')}\n\n<b>Familyasi</b>\n{data_dict.get('surname')}\n\n<b>Bog'lanish:</b>\n@{username}\n\n<b>O'qituvchisi</b>\n{data_dict.get('teacher')}\n\n<b>Dars soati</b>\n{data_dict.get('hour')}\n\n<b>Dars kunlari</b>\n{data_dict.get('days')}\n\n<b>Telefo'n raqami</b>\n{data_dict.get('number')}"
                    await bot.send_message(GROUP_ID, message_to_gr)
                else:
                    message_to_gr = f"<b>Qarzdorlikni tekshirish</b>\n\n<b>Ismi</b>\n{data_dict.get('name')}\n\n<b>Familyasi</b>\n{data_dict.get('surname')}\n\n<b>O'qituvchisi</b>\n{data_dict.get('teacher')}\n\n<b>Dars soati</b>\n{data_dict.get('hour')}\n\n<b>Dars kunlari</b>\n{data_dict.get('days')}\n\n<b>Telefo'n raqami</b>\n{data_dict.get('number')}"
                    if username:
                        message_to_gr = f"<b>Qarzdorlikni tekshirish</b>\n\n<b>Ismi</b>\n{data_dict.get('name')}\n\n<b>Familyasi</b>\n{data_dict.get('surname')}\n\n<b>Bog'lanish:</b>\n@{username}\n\n<b>O'qituvchisi</b>\n{data_dict.get('teacher')}\n\n<b>Dars soati</b>\n{data_dict.get('hour')}\n\n<b>Dars kunlari</b>\n{data_dict.get('days')}\n\n<b>Telefo'n raqami</b>\n{data_dict.get('number')}"
                    await bot.send_message(GROUP_ID, message_to_gr)
                data.clear()
            else:
                await message.answer("Введите правильный номер телефона")


@dp.message_handler(state=Comment.name)
async def comment_name(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=connect_menu())
        else:
            if len(user_msg.lower()) >= 3 and user_msg.isalpha():
                data['name'] = user_msg
                await Comment.next()
                await message.answer("Введите свою фамилию")
            else:
                await message.answer("Введите правильно")


@dp.message_handler(state=Comment.surname)
async def comment_surname(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=connect_menu())
        else:
            if len(user_msg.lower()) >= 3 and user_msg.isalpha():
                data['surname'] = user_msg
                await Comment.next()
                await message.answer("Введите ваш номер телефона")
            else:
                await message.answer("Введите правильно")


@dp.message_handler(state=Comment.number)
async def comment_number(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=connect_menu())
        else:
            if user_msg.strip("+").isdigit() and len(user_msg.strip("+")) == 9 or len(user_msg.strip("+")) == 12 and "." not in user_msg.strip("+"):
                data['number'] = user_msg
                await Comment.next()
                await message.answer("Вы можете оставить комментарий")
            else:
                await message.answer("Введите правильный номер телефона")


@dp.message_handler(state=Comment.comment)
async def comment_comment(message: types.Message, state: FSMContext):
    user_msg = message.text
    username = message.chat.username
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=connect_menu())
        else:
            data['comment'] = user_msg
            await message.answer("Здравствуйте! Благодарим вас за отзыв. Мы всегда стремимся улучшить наши услуги.", reply_markup=connect_menu())
            await state.finish()
            data_dict = data.as_dict()
            message_to_gr = f"<b>Yangi fikr</b>\n\n<b>Ismi</b>\n{data_dict.get('name')}\n\n<b>Familyasi</b>\n{data_dict.get('surname')}\n\n<b>Telefo'n raqami</b>\n{data_dict.get('number')}\n\n<b>Fikr</b>\n{data_dict.get('comment')}"
            if username:
                message_to_gr = f"<b>Yangi fikr</b>\n\n<b>Ismi</b>\n{data_dict.get('name')}\n\n<b>Familyasi</b>\n{data_dict.get('surname')}\n\n<b>Bog'lanish:</b>\n@{username}\n\n<b>Telefo'n raqami</b>\n{data_dict.get('number')}\n\n<b>Fikr</b>\n{data_dict.get('comment')}"
            await bot.send_message(GROUP_ID, message_to_gr)
            data.clear()


@dp.message_handler(state=Registration.name)
async def registration_name(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=start_menu())
        else:
            if len(user_msg.lower()) >= 3 and user_msg.isalpha():
                data['name'] = user_msg
                await Registration.next()
                await message.answer("Введите свою фамилию")
            else:
                await message.answer("Введите правильно")


@dp.message_handler(state=Registration.surname)
async def registration_surname(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=start_menu())
        else:
            if len(user_msg.lower()) >= 3 and user_msg.isalpha():
                data['surname'] = user_msg
                await Registration.next()
                await message.answer("Ваш номер телефона для связи?")
            else:
                await message.answer("Введите правильно")


@dp.message_handler(state=Registration.number1)
async def registration_number1(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=start_menu())
        else:
            if user_msg.strip("+").isdigit() and len(user_msg.strip("+")) == 9 or len(user_msg.strip("+")) == 12 and "." not in user_msg.strip("+"):
                data['number1'] = user_msg
                await Registration.next()
                await message.answer("Еще один номер, а вдруг не дозвонимся")
            else:
                await message.answer("Введите правильный номер телефона")


@dp.message_handler(state=Registration.number2)
async def registration_number2(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=start_menu())
        else:
            if user_msg.strip("+").isdigit() and len(user_msg.strip("+")) == 9 or len(user_msg.strip("+")) == 12 and "." not in user_msg.strip("+"):
                if data.get('number1')[::-1][0:9] != user_msg.strip("+")[::-1][0:9]:
                    data['number2'] = user_msg
                    await Registration.next()
                    await message.answer("Какие курсы вас интересуют?", reply_markup=cours_menu())
                else:
                    await message.answer("Первый номер телефона не должен совпадать с номером")
            else:
                await message.answer("Введите правильный номер телефона")


@dp.message_handler(state=Registration.course)
async def registration_course(message: types.Message, state: FSMContext):
    user_msg = message.text
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=start_menu())
        else:
            courses = []
            for course in get_course_category():
                courses.append(course[0].lower())
            if user_msg.lower() in courses:
                data['category'] = user_msg
                await Registration.next()
                await message.answer('Напишите дополнительную информацию к вашей заявке или просто нажмите "Отправить заявку".', reply_markup=back_send())
            else:
                await message.answer("Какие курсы вас интересуют?", reply_markup=cours_menu())


@dp.message_handler(state=Registration.comment)
async def registration_comment(message: types.Message, state: FSMContext):
    user_msg = message.text
    username = message.chat.username
    async with state.proxy() as data:
        if user_msg.lower() == "🔙назад":
            await state.finish()
            await message.answer(f"Выберите категорию", reply_markup=start_menu())
        else:
            await state.finish()
            data_dict = data.as_dict()
            data_db = data_dict
            if username:
                data_db['username'] = username
            else:
                data_db['username'] = "None"
            data_db['userid'] = message.chat.id
            status = create_student(data_db)
            if message.text.lower() == "отправить заявку":
                if status == 201:
                    message_to_group = f"<b>Yangi o'quvchi:</b>\n\n<b>Ismi:</b>\n{data_dict.get('name')}\n\n<b>Familyasi:</b>\n{data_dict.get('surname')}\n\n<b>Telefo'n raqami1:</b>\n{data_dict.get('number1')}\n\n<b>Telefo'n raqami2:</b>\n{data_dict.get('number2')}\n\n<b>Kurs katego'riyasi:</b>\n{data_dict.get('category')}"
                    if username:
                        message_to_group = f"<b>Yangi o'quvchi:</b>\n\n<b>Ismi:</b>\n{data_dict.get('name')}\n\n<b>Familyasi:</b>\n{data_dict.get('surname')}\n\n<b>Bog'lanish:</b>\n@{username}\n\n<b>Telefo'n raqami1:</b>\n{data_dict.get('number1')}\n\n<b>Telefo'n raqami2:</b>\n{data_dict.get('number2')}\n\n<b>Kurs katego'riyasi:</b>\n{data_dict.get('category')}"
                    await bot.send_message(GROUP_ID, message_to_group)
                    await message.answer("Спасибо за вашу заявку. Мы скоро с вами свяжемся.", reply_markup=start_menu())
                else:
                    await message.answer("Что-то пошло не так, попробуйте еще раз", reply_markup=start_menu())
            else:
                data['comment'] = user_msg
                data_dict = data.as_dict()
                if status == 201:
                    message_to_group = f"<b>Yangi o'quvchi:</b>\n\n<b>Ismi:</b>\n{data_dict.get('name')}\n\n<b>Familyasi:</b>\n{data_dict.get('surname')}\n\n<b>Telefo'n raqami1:</b>\n{data_dict.get('number1')}\n\n<b>Telefo'n raqami2:</b>\n{data_dict.get('number2')}\n\n<b>Tanlagan kurs katego'riyasi:</b>\n{data_dict.get('category')}\n\n<b>Qo'shimcha habar:</b>\n{data_dict.get('comment')}"
                    if username:
                        message_to_group = f"<b>Yangi o'quvchi:</b>\n\n<b>Ismi:</b>\n{data_dict.get('name')}\n\n<b>Familyasi:</b>\n{data_dict.get('surname')}\n\n<b>Bog'lanish:</b>\n@{username}\n\n<b>Telefo'n raqami1:</b>\n{data_dict.get('number1')}\n\n<b>Telefo'n raqami2:</b>\n{data_dict.get('number2')}\n\n<b>Tanlagan kurs katego'riyasi:</b>\n{data_dict.get('category')}\n\n<b>Qo'shimcha habar:</b>\n{data_dict.get('comment')}"
                    await bot.send_message(GROUP_ID, message_to_group)
                    await message.answer("Спасибо за вашу заявку. Мы скоро с вами свяжемся.", reply_markup=start_menu())
                else:
                    await message.answer("Что-то пошло не так, попробуйте еще раз", reply_markup=start_menu())
            data.clear()
