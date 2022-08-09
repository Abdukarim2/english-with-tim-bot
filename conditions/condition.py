from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp,bot
from messages.message import MESSAGES as M
from keyboards.reply import four_row, remove, back
from keyboards.inline import inlines
from states.state import Courses, AddCourseTeacher, UserRegistration, CommentState, CheckStudent
from configs.config import BASE_DIR, ADMIN_ID, ADMIN_ID2
from utils.database import Database


@dp.message_handler(commands=['start', 'начать'])
async def commands(message: types.Message):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        await message.answer(M.get('start').get('msg')[0])
        await message.answer("Выберите категорию", reply_markup=four_row(M.get('start').get('btns')))


@dp.message_handler(commands=['add_course'])
async def add_course(message: types.Message, state: FSMContext):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        if message.chat.id == ADMIN_ID or message.chat.id == ADMIN_ID2:
            async with state.proxy() as data:
                data['table'] = "courses"
                await message.answer("Kurs nomini kiritn", reply_markup=remove())
            await AddCourseTeacher.name.set()
        else:
            await message.answer("Kechirasiz siz admin emassiz!!!")


@dp.message_handler(commands=['del_course'])
async def delete_course(message: types.Message):
    db = Database()
    if message.chat.type != "group" and message.chat.type != "supergroup":
        if message.chat.id == ADMIN_ID or message.chat.id == ADMIN_ID2:
            courses = db.courses_teachers(table_name="courses", category='', all=True)
            markup = inlines(words=courses, delete="del_course_")
            await message.answer("O'chirish uchun kursni tanlang", reply_markup=markup)
    else:
        await message.answer("Kechirasiz siz admin emassiz!!!")


@dp.message_handler(commands=['del_teacher'])
async def delete_teacher(message: types.Message):
    db = Database()
    if message.chat.type != "group" and message.chat.type != "supergroup":
        if message.chat.id == ADMIN_ID or message.chat.id == ADMIN_ID2:
            courses = db.courses_teachers(table_name="teachers", category='', all=True)
            markup = inlines(words=courses, delete="del_teacher_")
            await message.answer("O'chirish uchun o'qituvchi tanlang tanlang", reply_markup=markup)
    else:
        await message.answer("Kechirasiz siz admin emassiz!!!")


@dp.message_handler(commands=['help'])
async def delete_teacher(message: types.Message):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        if message.chat.id == ADMIN_ID or message.chat.id == ADMIN_ID2:
            await message.answer("/add_teacher Yangi o'qituvchi qo'shish\n/del_teacher O'qituvchini o'chirish\n/add_course Yangi kurs qo'shsih\n/del_course Kursni o'chirish\n/get_students O'quvchilarni olish\n/del_student O'quvchini o'chirish")
    else:
        await message.answer("Выберите категорию!!!")


@dp.message_handler(commands=['add_teacher'])
async def add_teacher(message: types.Message, state: FSMContext):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        if message.chat.id == ADMIN_ID or message.chat.id == ADMIN_ID2:
            async with state.proxy() as data:
                data['table'] = "teachers"
                await message.answer("O'qituvchi ismini kiritn", reply_markup=remove())
            await AddCourseTeacher.name.set()
        else:
            await message.answer("Kechirasiz siz admin emassiz!!!")


@dp.message_handler(commands=['get_students'])
async def get_student(message: types.Message, state: FSMContext):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        if message.chat.id == ADMIN_ID or message.chat.id == ADMIN_ID2:
            async with state.proxy() as data:
                data['table'] = "students"
                data['back_to'] = "start"
                await message.answer("Kategoriyadan tanlang", reply_markup=four_row(M.get('category').get("btns")))
            await Courses.name.set()
        else:
            await message.answer("Kechirasiz siz admin emassiz!!!")

@dp.message_handler(commands=['del_student'])
async def delete_student(message: types.Message, state: FSMContext):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        if message.chat.id == ADMIN_ID or message.chat.id == ADMIN_ID2:
            async with state.proxy() as data:
                data['table'] = "del_student"
                data['back_to'] = "start"
            await message.answer("Kategoriyadan tanlang", reply_markup=four_row(M.get('category').get("btns")))
            await Courses.name.set()
    else:
        await message.answer("Kechirasiz siz admin emassiz!!!")

@dp.message_handler()
async def messages(message: types.Message,  state: FSMContext):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        l_msg_text = message.text.lower()
        # start command conditions
        start_msg = M.get('start')
        about_msg = M.get('about')
        connext_msg = M.get('connect')
        if l_msg_text == start_msg.get('btns')[0].lower():
            for word in M.get('about').get('msg'):
                await message.answer(word)
            await message.answer('Выберите категорию', reply_markup=four_row(M.get('about').get('btns')))
        elif l_msg_text == start_msg.get('btns')[1].lower():
            await message.answer('Выберите категорию', reply_markup=four_row(M.get('connect').get('btns')))
        elif l_msg_text == start_msg.get('btns')[2].lower():
            await message.answer("Как нам вас называть?", reply_markup=back())
            await UserRegistration.name.set()
        elif l_msg_text == start_msg.get('btns')[3].lower():
            await message.answer("Телефонные номера:\n1: +998 90 528 88 77\n2: +998 90 528 88 00")
            await message.answer_location(latitude=40.7600858, longitude=72.3490069)
            await message.answer("Инстаграм https://www.instagram.com/english_with_tim")
            await message.answer("Телеграмм канал https://t.me/ENGwTim")
            await message.answer("С вопросами обращайтесь по этому @English_with_Tim_support телеграмм тегу")
        # about command condition
        elif l_msg_text == about_msg.get("btns")[0].lower():
            await message.answer('Выберите категорию', reply_markup=four_row(M.get('category').get("btns")))
            async with state.proxy() as data:
                data['back_to'] = "about"
                data['table'] = "courses"
            await Courses.name.set()
        elif l_msg_text == about_msg.get("btns")[1].lower():
            await message.answer('Выберите категорию', reply_markup=four_row(M.get('category').get("btns")))
            async with state.proxy() as data:
                data['back_to'] = "about"
                data['table'] = "teachers"
            await Courses.name.set()
        elif l_msg_text == about_msg.get("btns")[2].lower():
            await message.answer_photo(
                open(BASE_DIR / "images/price.png", 'rb'),
                caption=message.text
            )
        # connect commands
        elif l_msg_text == connext_msg.get("btns")[0].lower():
            async with state.proxy() as data:
                data['debt'] = True
            await message.answer("Введите своё имя", reply_markup=back())
            await CheckStudent.name.set()
        elif l_msg_text == connext_msg.get("btns")[1].lower():
            async with state.proxy() as data:
                data['debt'] = False
            await message.answer("Введите своё имя", reply_markup=back())
            await CheckStudent.name.set()
        elif l_msg_text == connext_msg.get("btns")[2].lower():
            await message.answer("Введите своё имя", reply_markup=back())
            await CommentState.name.set()
        # back to
        elif l_msg_text == "🔙назад":
            await message.answer("Выберите категорию", reply_markup=four_row(M.get('start').get('btns')))


@dp.callback_query_handler(lambda call: True)
async def delete(message: types.CallbackQuery):
    db = Database()
    if message.data.startswith("del_course_"):
        data = message.data[11:]
        deleting = db.delete_db("courses", data)
        if deleting == 200:
            await bot.edit_message_text(f"Muvofaqiyatlik o'chirildi", message.from_user.id, message.message.message_id)
        else:
            await bot.edit_message_text(f"Nimadur hato ketdi boshqatdan urinib ko'rin", message.from_user.id, message.message.message_id)
    elif message.data.startswith("del_teacher_"):
        data = message.data[12:]
        deleting = db.delete_db("teachers", data)
        if deleting == 200:
            await bot.edit_message_text(f"Muvofaqiyatlik o'chirildi", message.from_user.id, message.message.message_id)
        else:
            await bot.edit_message_text(f"Nimadur hato ketdi boshqatdan urinib ko'rin", message.from_user.id, message.message.message_id)

