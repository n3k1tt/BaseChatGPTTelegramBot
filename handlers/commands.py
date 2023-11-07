from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject

router = Router()  # [1]

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    await message.answer(
        "Привет, Я бот для общения с GPT для того чтобы задать вопрос просто напишщи сообщение"
    )
@router.message(Command("help"))
async def cmd_start(message: types.Message, command: CommandObject):
    await message.answer("Возможные команды: \n /memory - просмотр истории общения с GPT \n /clearmemory - очистить память о сообщениях \n /change - замена модели возможные аргументы 'gpt-3.5-turbo','gpt-4'")
