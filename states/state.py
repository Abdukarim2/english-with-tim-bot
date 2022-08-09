from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp, bot
from messages.message import MESSAGES as M
from keyboards.reply import four_row, three_row, back
from keyboards.inline import inlines
from utils.database import Database
from configs.config import GROUP_ID


class Courses(StatesGroup):
    name = State()


class ChooseTeacher(StatesGroup):
    name = State()

class AddCourseTeacher(StatesGroup):
    name = State()
    about = State()
    category = State()


class UserRegistration(StatesGroup):
    name = State()
    surname = State()
    phone1 = State()
    phone2 = State()
    course = State()
    comment = State()


class CommentState(StatesGroup):
    name = State()
    surname = State()
    number = State()
    comment = State()


class CheckStudent(StatesGroup):
    name = State()
    surname = State()
    teacher = State()
    date = State()
    days = State()
    number = State()


@dp.message_handler(state=Courses.name)
async def choose_category(message: types.Message, state: FSMContext):
    db = Database()
    async with state.proxy() as data:
        if message.text in M.get('category').get("btns"):
            if message.text == "🔙Назад":
                await state.finish()
                await message.answer("Выберите категорию",
                                     reply_markup=four_row(
                                         M.get(f"{data['back_to']}").get("btns")
                                            ))
            else:
                if data['table'] == "courses":
                    courses = db.courses_teachers(table_name=f"courses", category=message.text)
                    for course in courses:
                        await message.answer(f"<b>{course[1]}</b>\n{course[2]}")
                elif data['table'] == "teachers":
                    teachers = db.courses_teachers(table_name="teachers", category=message.text)
                    markup = inlines(words=teachers, delete="choose_teachers_")
                    await message.answer("Выберите имя учителя", reply_markup=markup)
                elif data['table'] == "students":
                    students = db.users(category=message.text)
                    if len(students) != 0:
                        markup = inlines(words=students, delete="get_students_")
                        await message.answer("O'quvchini tanlang", reply_markup=markup)
                    else:
                        await message.answer(f"{message.text} da o'quvchi topilmadi🤷‍♂️")
                elif data['table'] == "del_student":
                    students = db.users(category=message.text)
                    if len(students) != 0:
                        markup = inlines(words=students, delete="del_student_")
                        await message.answer("O'quvchini tanlang", reply_markup=markup)
                    else:
                        await message.answer(f"{message.text} da o'quvchi topilmadi🤷‍♂️")
        else:
            await message.answer("Выберите категорию",
                                 reply_markup=four_row(M.get('category').get("btns")))


@dp.message_handler(state=AddCourseTeacher.name)
async def add_course_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        text = "Kurs haqida matn kiritn" if data['table'] == "courses" \
                                         else "O'qituvchi haqida matn kiritn"

        await message.answer(text)
        await AddCourseTeacher.next()


@dp.message_handler(state=AddCourseTeacher.about)
async def add_course_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['about'] = message.text
        text = "Kurs kategoriyasini tnlang" if data['table'] == "courses" \
            else "O'qituvchi kategoriyasini tnlang"
        await message.answer(text,
                             reply_markup=three_row(M.get('category').get("btns")[0:3]))
        await AddCourseTeacher.next()


@dp.message_handler(state=AddCourseTeacher.category)
async def add_course_category(message: types.Message, state: FSMContext):
    db = Database()
    async with state.proxy() as data:
        if message.text in M.get('category').get("btns")[0:3]:
            creating = db.courses_teachers(table_name=f"{data['table']}", category=message.text, name=data['name'], about=data['about'])
            if creating == 200:
                await message.answer("Muvofaqiyatlik qo'shildi", reply_markup=four_row(M.get('start').get('btns')))
                await state.finish()
            else:
                await message.answer("Nimadur hato ketdi boshqatdan urining", reply_markup=four_row(M.get('start').get('btns')))
                await state.finish()
        else:
            await message.answer("Kurs kategoriyasini tnlang",
                                 reply_markup=three_row(M.get('category').get("btns")[0:3]))


@dp.message_handler(state=UserRegistration.name)
async def user_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('start').get('btns')))
        else:
            data['name'] = message.text
            await message.answer("Можно и фамилию?")
            await UserRegistration.next()


@dp.message_handler(state=UserRegistration.surname)
async def user_sur(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('start').get('btns')))
        else:
            data['surname'] = message.text
            await message.answer("Ваш номер телефона для связи?")
            await UserRegistration.next()


@dp.message_handler(state=UserRegistration.phone1)
async def user_ph1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('start').get('btns')))
        else:
            if message.text.strip("+").isdigit() and len(message.text.strip("+")) == 9 or len(message.text.strip("+")) == 12 and "." not in message.text.strip("+"):
                data['phone1'] = message.text
                await message.answer("Еще один номер, а вдруг не дозвонимся")
                await UserRegistration.next()
            else:
                await message.answer("Введите правильный номер телефона")

@dp.message_handler(state=UserRegistration.phone2)
async def user_ph2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('start').get('btns')))
        else:
            if message.text.strip("+").isdigit() and len(message.text.strip("+")) == 9 or len(message.text.strip("+")) == 12 and "." not in message.text.strip("+"):
                if data.get('phone1')[::-1][0:9] != message.text.strip("+")[::-1][0:9]:
                    data['phone2'] = message.text
                    await message.answer("Какие курсы вас интересуют?",
                                         reply_markup=four_row(M.get("category").get("btns"), one_time=True))
                    await UserRegistration.next()
                else:
                    await message.answer("Первый номер телефона не должен совпадать с номером")
            else:
                await message.answer("Введите правильный номер телефона")


@dp.message_handler(state=UserRegistration.course)
async def user_course(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('start').get('btns')))
        else:
            if message.text in M.get('category').get("btns")[0:3]:
                data['course'] = message.text
                await message.answer("Напишите дополнительную информацию к вашей заявке или просто нажмите \"🧑‍💻Отправить заявку\".", reply_markup=back(additional=True))
                await UserRegistration.next()
            else:
                await message.answer("Какие курсы вас интересуют?")


@dp.message_handler(state=UserRegistration.comment)
async def user_course(message: types.Message, state: FSMContext):
    db = Database()
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('start').get('btns')))
        else:
            creating = db.users(
                str(data['name']),
                str(data['surname']),
                int(data['phone1']),
                int(data['phone2']),
                str(message.chat.username),
                str(data['course']))
            if creating == 200:
                if message.text.lower() == "🧑‍💻отправить заявку":
                    await message.answer("Спасибо за вашу заявку. Мы скоро с вами свяжемся. ", reply_markup=four_row(M.get('start').get('btns')))
                    message_to_group = f"<b>Yangi o'quvchi:</b>\n\n<b>Ismi:</b>\n{data['name']}\n\n<b>Familyasi:</b>\n{data['surname']}\n\n<b>Bog'lanish:</b>\n@{message.chat.username}\n\n<b>Telefo'n raqami1:</b>\n{data['phone1']}\n\n<b>Telefo'n raqami2:</b>\n{data['phone2']}\n\n<b>Tanlagan kursi:</b>\n{data['course']}"
                    await bot.send_message(GROUP_ID, message_to_group)
                else:
                    message_to_group = f"<b>Yangi o'quvchi:</b>\n\n<b>Ismi:</b>\n{data['name']}\n\n<b>Familyasi:</b>\n{data['surname']}\n\n<b>Bog'lanish:</b>\n@{message.chat.username}\n\n<b>Telefo'n raqami1:</b>\n{data['phone1']}\n\n<b>Telefo'n raqami2:</b>\n{data['phone2']}\n\n<b>Tanlagan kursi:</b>\n{data['course']}\n\n<b>Qo'shimcha habar:</b>\n{message.text}"
                    await bot.send_message(GROUP_ID, message_to_group)
                    await message.answer("Спасибо за вашу заявку. Мы скоро с вами свяжемся. ", reply_markup=four_row(M.get('start').get('btns')))
            else:
                await message.answer("Что-то пошло не так, попробуйте еще раз",reply_markup=four_row(M.get('start').get('btns')))
            await state.finish()


@dp.message_handler(state=CommentState.name)
async def comment_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
        else:
            data['name'] = message.text
            await message.answer("Введите свою фамилию")
            await CommentState.next()


@dp.message_handler(state=CommentState.surname)
async def comment_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
        else:
            data['surname'] = message.text
            await message.answer("Введите ваш номер телефона")
            await CommentState.next()


@dp.message_handler(state=CommentState.number)
async def comment_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
        else:
            if message.text.strip("+").isdigit() and len(message.text.strip("+")) == 9 or len(message.text.strip("+")) == 12 and "." not in message.text.strip("+"):
                data['number'] = message.text
                await message.answer("Вы можете оставить комментарий")
                await CommentState.next()
            else:
                await message.answer("Введите правильный номер телефона")


@dp.message_handler(state=CommentState.comment)
async def comment_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
        else:
            message_to_gr = f"<b>Yangi fikr</b>\n\n<b>Ismi</b>\n{data['name']}\n\n<b>Familyasi</b>\n{data['surname']}\n\n<b>Telefo'n raqami</b>\n{data['number']}\n\n<b>Fikr</b>\n{message.text}"
            await bot.send_message(GROUP_ID, message_to_gr)
            await message.answer("Здравствуйте! Благодарим вас за отзыв. Мы всегда стремимся улучшить наши услуги.", reply_markup=four_row(M.get('connect').get('btns')))
            await state.finish()


@dp.message_handler(state=CheckStudent.name)
async def check_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
        else:
            data['name'] = message.text
            await message.answer("Введите свою фамилию")
            await CheckStudent.next()


@dp.message_handler(state=CheckStudent.surname)
async def check_surname(message: types.Message, state: FSMContext):
    db = Database()
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
        else:
            teachers_db = db.courses_teachers(table_name="teachers", category='', all=True)
            data['surname'] = message.text
            await message.answer("У кого вы учитесь?\nВыберите имя учителя", reply_markup=inlines(teachers_db))
            await CheckStudent.next()


@dp.callback_query_handler(lambda call: True, state=CheckStudent.teacher)
async def check_teacher_call(message: types.CallbackQuery, state: FSMContext):
    teacher = message.data[9:]
    async with state.proxy() as data:
        data['teacher'] = teacher
        await bot.edit_message_text("Во сколько начинаются ваши уроки? ",
                                    message.from_user.id, message.message.message_id,
                                    reply_markup=inlines(M.get("dates").get("btns")))
        await CheckStudent.next()


@dp.message_handler(state=CheckStudent.teacher)
async def check_teacher(message: types.Message, state: FSMContext):
    if message.text.lower() == "🔙назад":
        await state.finish()
        await message.delete()
        await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
    else:
        await message.answer("Выберите имя учителя", reply_markup=inlines(M.get("dates").get("btns")))


@dp.callback_query_handler(lambda call: True, state=CheckStudent.date)
async def check_date_call(message: types.CallbackQuery, state: FSMContext):
    date = message.data[9:]
    async with state.proxy() as data:
        data['date'] = date
        await bot.edit_message_text("В какие дни вы приходите на курсы?", message.from_user.id, message.message.message_id,
                                    reply_markup=inlines(M.get("days").get("btns")))
        await CheckStudent.next()


@dp.message_handler(state=CheckStudent.date)
async def check_date(message: types.Message, state: FSMContext):
    if message.text.lower() == "🔙назад":
        await state.finish()
        await message.delete()
        await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
    else:
        await message.answer("Во сколько начинаются ваши уроки?", reply_markup=inlines(M.get("dates").get("btns")))


@dp.callback_query_handler(lambda call: True, state=CheckStudent.days)
async def check_days_call(message: types.CallbackQuery, state: FSMContext):
    days = message.data[9:]
    async with state.proxy() as data:
        data['days'] = days
        await bot.edit_message_text("Введите ваш номер телефона", message.from_user.id, message.message.message_id)
        await CheckStudent.next()


@dp.message_handler(state=CheckStudent.days)
async def check_days(message: types.Message, state: FSMContext):
    if message.text.lower() == "🔙назад":
        await state.finish()
        await message.delete()
        await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
    else:
        await message.answer("В какие дни вы приходите на курсы?", reply_markup=inlines(M.get("days").get("btns")))


@dp.message_handler(state=CheckStudent.number)
async def check_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "🔙назад":
            await state.finish()
            await message.delete()
            await message.answer(message.text, reply_markup=four_row(M.get('connect').get('btns')))
        else:
            if message.text.strip("+").isdigit() and len(message.text.strip("+")) == 9 or len(message.text.strip("+")) == 12 and "." not in message.text.strip("+"):
                if data.get("debt"):
                    message_to_gr = f"<b>Qarzdorlikni tekshirish</b>\n\n<b>Ismi</b>\n{data['name']}\n\n<b>Familyasi</b>\n{data['surname']}\n\n<b>O'qituvchisi</b>\n{data['teacher']}\n\n<b>Dars soati</b>\n{data['date']}\n\n<b>Dars kunlari</b>\n{data['days']}\n\n<b>Telefo'n raqami</b>\n{message.text}"
                    await bot.send_message(GROUP_ID, message_to_gr)
                else:
                    message_to_gr = f"<b>Davomadni tekshirish</b>\n\n<b>Ismi</b>\n{data['name']}\n\n<b>Familyasi</b>\n{data['surname']}\n\n<b>O'qituvchisi</b>\n{data['teacher']}\n\n<b>Dars soati</b>\n{data['date']}\n\n<b>Dars kunlari</b>\n{data['days']}\n\n<b>Telefo'n raqami</b>\n{message.text}"
                    await bot.send_message(GROUP_ID, message_to_gr)
                await message.answer("Ваш запрос успешно отправлен. Мы скоро с вами свяжемся", reply_markup=four_row(M.get('start').get('btns')))
                await state.finish()
            else:
                await message.answer("Введите правильный номер телефона")


@dp.callback_query_handler(lambda call: True, state=Courses.name)
async def choose_teachers(message: types.CallbackQuery, state: FSMContext):
    db = Database()
    if message.data.startswith("choose_teachers_"):
        teacher = message.data[16:]
        reslut = db.choose(table_name="teachers", where=f"{teacher}")
        await bot.edit_message_text(f"<b>{reslut[1]}</b>\n{reslut[2]}", message.from_user.id, message.message.message_id)
    elif message.data.startswith("get_students_"):
        student = message.data[13:]
        result = db.choose(table_name="users", where=f"{student}")
        await bot.edit_message_text(f"<b>Ismi:</b>\n{result[1]}\n\n<b>Familyasi:</b>\n{result[2]}\n\n<b>telefo'n1:</b>\n+{result[3]}\n\n<b>telefo'n2:</b>\n+{result[4]}\n\n<b>bog'lanish:</b>\n@{result[5]}\n\n<b>Kursi:</b>\n{result[6]}", message.from_user.id,
                                    message.message.message_id)
    elif message.data.startswith("del_student_"):
        student = message.data[12:]
        await bot.send_message(message.from_user.id,student)
        deleting = db.choose(table_name="users", where=student, delete=True)
        if deleting == 200:
            await bot.edit_message_text(f"Muvofaqiyatlik o'chirildi", message.from_user.id, message.message.message_id)
        else:
            await bot.edit_message_text(f"Nimadur hato ketdi boshqatdan urinib ko'rin", message.from_user.id, message.message.message_id)
