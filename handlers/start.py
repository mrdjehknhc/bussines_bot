from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import init_db

# Главное меню
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📦 Склад"),
        KeyboardButton("💰 Продажи")
    ).add(
        KeyboardButton("📊 Финансы"),
        KeyboardButton("📝 Заметки"),
        KeyboardButton("⚙️ Настройки")
    )
    return kb

# Команда /start
async def cmd_start(message: types.Message):
    init_db()  # инициализация БД при старте
    await message.answer(
        "👋 Добро пожаловать в бот учёта продаж!\nВыберите раздел:",
        reply_markup=main_menu()
    )

# Обработка нажатий на кнопки главного меню
async def handle_main_menu(message: types.Message):
    text = message.text
    if text == "📦 Склад":
        await message.answer("Раздел 📦 СКЛАД. Доступные команды:\n/добавить_позицию\n/редактировать_позицию\n/удалить_позицию\n/склад")
    elif text == "💰 Продажи":
        await message.answer("Раздел 💰 ПРОДАЖИ. Доступные команды:\n/новая_продажа\n/продажи\n/возврат")
    elif text == "📊 Финансы":
        await message.answer("Раздел 📊 ФИНАНСЫ. Отчёты и аналитика.")
    elif text == "📝 Заметки":
        await message.answer("Раздел 📝 ЗАМЕТКИ. Создавайте и просматривайте записи.")
    elif text == "⚙️ Настройки":
        await message.answer("Раздел ⚙️ НАСТРОЙКИ. Управление валютой и напоминаниями.")
    else:
        await message.answer("Пожалуйста, выбери один из разделов на клавиатуре.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(handle_main_menu)
