from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import get_all_products, reduce_stock, add_sale
from keyboards.inline import get_products_keyboard
from utils.filters import extract_variation_input

class NewSale(StatesGroup):
    product = State()
    variation = State()
    quantity = State()
    price = State()
    platform = State()
    date = State()
    comment = State()

# /новая_продажа
async def cmd_new_sale(message: types.Message):
    products = get_all_products()
    if not products:
        await message.answer("Склад пуст. Добавьте товар перед продажей.")
        return

    kb = get_products_keyboard(products)
    await message.answer("Выберите товар для продажи:", reply_markup=kb)
    await NewSale.product.set()

async def select_product(callback: types.CallbackQuery, state: FSMContext):
    product_name = callback.data
    await state.update_data(product=product_name)
    await callback.message.edit_text("Введите цвет / размер (например: Белый / M):")
    await NewSale.variation.set()

async def process_variation(message: types.Message, state: FSMContext):
    variation = extract_variation_input(message.text)
    if not variation:
        await message.answer("Неверный формат. Введите, например: Чёрный / L")
        return

    await state.update_data(variation=variation)
    await message.answer("Введите количество:")
    await NewSale.quantity.set()

async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
        await state.update_data(quantity=quantity)
        await message.answer("Введите цену продажи за 1 шт:")
        await NewSale.price.set()
    except ValueError:
        await message.answer("Введите число.")

async def process_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await message.answer("Укажите площадку: OLX / Vinted / Facebook / другое")
        await NewSale.platform.set()
    except ValueError:
        await message.answer("Введите число.")

async def process_platform(message: types.Message, state: FSMContext):
    await state.update_data(platform=message.text)
    await message.answer("Дата продажи (в формате ГГГГ-ММ-ДД или 'сегодня'):")
    await NewSale.date.set()

async def process_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text if message.text != "сегодня" else None)
    await message.answer("Комментарий (опционально):")
    await NewSale.comment.set()

async def process_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    comment = message.text

    # Обновить склад и зафиксировать продажу
    result = reduce_stock(
        name=data['product'],
        variation=data['variation'],
        quantity=data['quantity']
    )

    if not result:
        await message.answer("Ошибка: недостаточно товара на складе.")
        await state.finish()
        return

    add_sale(
        name=data['product'],
        variation=data['variation'],
        quantity=data['quantity'],
        price=data['price'],
        platform=data['platform'],
        date=data['date'],
        comment=comment
    )

    await message.answer("✅ Продажа успешно зафиксирована.")
    await state.finish()

def register_handlers_sales(dp: Dispatcher):
    dp.register_message_handler(cmd_new_sale, commands=["новая_продажа"])
    dp.register_callback_query_handler(select_product, state=NewSale.product)
    dp.register_message_handler(process_variation, state=NewSale.variation)
    dp.register_message_handler(process_quantity, state=NewSale.quantity)
    dp.register_message_handler(process_price, state=NewSale.price)
    dp.register_message_handler(process_platform, state=NewSale.platform)
    dp.register_message_handler(process_date, state=NewSale.date)
    dp.register_message_handler(process_comment, state=NewSale.comment)
