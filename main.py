from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import init_db
from handlers import register_all_handlers
import logging

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Главный запуск
async def on_startup(dp):
    init_db()  # Инициализация БД
    print("Бот запущен и готов к работе!")

if __name__ == '__main__':
    register_all_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
