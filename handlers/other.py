import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import CommandObject
import g4f

router = Router()  # [1]
activeUsers = {}
allMemory = {}
settingsrouter = Router()


@settingsrouter.message(Command("memory"))
async def memory(message: Message):
    chat = message.chat
    names = {"assistant": "**GPT**", "user": "**You**"}
    if chat.id in allMemory:
        history = allMemory[chat.id]
        answer = ""
        for msg in history:
            phrase = names[msg['role']]+": "+msg['content']+"\n"
            answer += phrase
        await message.reply(answer)
    else:
        await message.reply("Бот не помнит ваши сообщения")


@settingsrouter.message(Command("clearmemory"))
async def clearmemory(message: Message):
    del allMemory[message.chat.id]
    await message.reply("Память очищена")


@settingsrouter.message(Command("change"))
async def changemodel(message: Message, command: CommandObject):
    models = {"gpt-4": g4f.models.gpt_4, "gpt-3.5-turbo": g4f.models.gpt_35_turbo, "code-davinci": g4f.models.code_davinci_002}
    chat = message.chat
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return

    if chat.id in activeUsers:
        pass
    else:
        activeUsers[chat.id] = {"last": datetime.datetime.now().timestamp() - 26, "model": g4f.models.gpt_35_turbo}
    if command.args in models:
        activeUsers[chat.id]['model'] = models[command.args]
        del allMemory[message.chat.id]
        await message.reply("Модель заменена на:**"+command.args+"**")
    else:
        await message.reply("Такой модели нету")


@router.message(F.text)
async def message_with_text(message: Message):
    global activeUsers
    starttime = datetime.datetime.now().timestamp()
    chat = message.chat
    if chat.id in activeUsers:
        pass
    else:
        activeUsers[chat.id] = {"last": datetime.datetime.now().timestamp()-26, "model": g4f.models.gpt_35_turbo}
    aftertime = activeUsers[chat.id]['last']+25-starttime
    if aftertime < 0:
        activeUsers[chat.id]['last'] = datetime.datetime.now().timestamp()
    else:
        await message.reply("25 секунд еще не прошли! Осталось еще: " + str(int(aftertime)))
        return
    msg = await message.reply("GPT Думает...")
    history = await get_memory(chat.id, {"role": "user", "content": message.text})
    request = await g4f.ChatCompletion.create_async(
        model=activeUsers[chat.id]['model'],
        messages=history,
    )
    # str=""
    # for i in range(len(request)):
    #     str=str+request[i]
    #     await msg.edit_text(str)
    attempts = 0
    if request == "":
        while request == "":
            request = await g4f.ChatCompletion.create_async(
                model="gpt-3.5-turbo",
                messages=history,
            )
            attempts += 1
            if attempts >= 10:
                await msg.edit_text("Извините, запрос не удался попробуйте позже")
                return
    await add_to_memory(chat.id, request)
    request += "\n\n ваш запрос выполнен за: " + str(round(datetime.datetime.now().timestamp()-starttime, 1)) + "с. \n Поддержка: @nikitoa \n Ответ выдан с использованием контекста \n Модель:"+activeUsers[chat.id]['model'].name
    await msg.edit_text(request)


async def get_memory(user_id, new):
    global allMemory
    if user_id in allMemory:
        allMemory[user_id].append(new)
    else:
        allMemory[user_id] = [new]
    return allMemory[user_id]


async def add_to_memory(user_id, new):
    global allMemory
    allMemory[user_id].append({"role": "assistant", "content": new})
