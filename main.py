from aiogram import executor, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import dp
from utils.db import init
from handlers import state_handler, message_handler, callback_handler


class GroupMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        if message.chat.type != "group" and message.chat.type != "supergroup":
            return True
        else:
            raise CancelHandler()


async def on_start(_):
    init()
    print("bot is runing...")


async def on_shutdown(_):
    print("bot is stoped")


if __name__ == "__main__":
    dp.middleware.setup(GroupMiddleware())
    executor.start_polling(dp, skip_updates=False, on_startup=on_start, on_shutdown=on_shutdown)
