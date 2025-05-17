from aiogram import types, Dispatcher
from database import get_finance_summary, get_sales_by_period
from datetime import datetime, timedelta

# /финансы
async def cmd_finances(message: types.Message):
    summary = get_finance_summary()

    response = (
        "📊 <b>Финансовый отчёт</b>\n\n"
        f"💰 Доходы: <b>{summary['income']:.2f}</b>\n"
        f"📦 Расходы: <b>{summary['expenses']:.2f}</b>\n"
        f"📈 Прибыль: <b>{summary['profit']:.2f}</b>\n"
        f"🚚 Доставка: <b>{summary['delivery']:.2f}</b>\n"
        f"📉 Средняя маржа: <b>{summary['avg_margin']:.2f}%</b>\n"
    )

    await message.answer(response, parse_mode="HTML")

# /отчет_неделя
async def cmd_weekly_report(message: types.Message):
    today = datetime.today().date()
    week_ago = today - timedelta(days=7)
    sales = get_sales_by_period(week_ago, today)

    if not sales:
        await message.answer("За последнюю неделю продаж не было.")
        return

    text = f"📆 Отчёт за неделю ({week_ago} — {today})\n\n"
    total = 0
    for s in sales:
        subtotal = s['quantity'] * s['price']
        total += subtotal
        text += f"{s['date']}: {s['name']} ({s['variation']}) x{s['quantity']} = {subtotal:.2f}\n"

    text += f"\n💵 <b>Всего: {total:.2f}</b>"
    await message.answer(text, parse_mode="HTML")

def register_handlers_finances(dp: Dispatcher):
    dp.register_message_handler(cmd_finances, commands=["финансы"])
    dp.register_message_handler(cmd_weekly_report, commands=["отчет_неделя"])
