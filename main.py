import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import commands,other
from config import TOKEN

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=TOKEN, parse_mode="MARKDOWN")
    dp = Dispatcher()

    dp.include_routers(commands.router, other.settingsrouter, other.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
