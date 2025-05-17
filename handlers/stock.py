from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import add_product, get_all_products, update_product, delete_product, get_product_by_name
from keyboards.inline import get_products_keyboard
from utils.filters import extract_stock_data

class AddProduct(StatesGroup):
    name = State()
    variations = State()
    price = State()
    delivery_cost = State()
    include_delivery = State()
    date = State()

# /добавить_позицию
async def cmd_add_position(message: types.Message):
    await message.answer("Введите название товара:")
    await AddProduct.name.set()

async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите цвет / размер / количество (по строчкам):\nПример:\nБелый / M / 20\nЧёрный / L / 30")
    await AddProduct.variations.set()

async def process_variations(message: types.Message, state: FSMContext):
    await state.update_data(variations=message.text)
    await message.answer("Введите цену закупа за 1 ед:")
    await AddProduct.price.set()

async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=float(message.text))
    await message.answer("Введите стоимость доставки всей партии:")
    await AddProduct.delivery_cost.set()

async def process_delivery(message: types.Message, state: FSMContext):
    await state.update_data(delivery=float(message.text))
    await message.answer("Учитывать доставку в себестоимости? (Да / Нет)")
    await AddProduct.include_delivery.set()

async def process_include_delivery(message: types.Message, state: FSMContext):
    await state.update_data(include_delivery=message.text.lower() == "да")
    await message.answer("Введите дату поступления (формат ГГГГ-ММ-ДД) или отправьте 'сегодня':")
    await AddProduct.date.set()

async def process_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    variations = extract_stock_data(data['variations'])
    price = data['price']
    delivery = data['delivery']
    include_delivery = data['include_delivery']
    date = message.text if message.text != "сегодня" else None

    add_product(name, variations, price, delivery, include_delivery, date)
    await message.answer(f"Товар '{name}' успешно добавлен в склад ✅")
    await state.finish()

# /склад
async def cmd_show_stock(message: types.Message):
    products = get_all_products()
    if not products:
        await message.answer("Склад пуст ❌")
    else:
        text = "📦 Остатки на складе:\n\n"
        for p in products:
            text += f"🔹 {p['name']}:\n"
            for v in p['variations']:
                text += f"  • {v['color']} / {v['size']} — {v['quantity']} шт\n"
        await message.answer(text)

def register_handlers_stock(dp: Dispatcher):
    dp.register_message_handler(cmd_add_position, commands=['добавить_позицию'])
    dp.register_message_handler(cmd_show_stock, commands=['склад'])
    dp.register_message_handler(process_name, state=AddProduct.name)
    dp.register_message_handler(process_variations, state=AddProduct.variations)
    dp.register_message_handler(process_price, state=AddProduct.price)
    dp.register_message_handler(process_delivery, state=AddProduct.delivery_cost)
    dp.register_message_handler(process_include_delivery, state=AddProduct.include_delivery)
    dp.register_message_handler(process_date, state=AddProduct.date)
