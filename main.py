from aiogram import executor
from loader import dp
from conditions import condition
from states import state

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
