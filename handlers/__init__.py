from aiogram import Dispatcher

from .start import register_handlers_start
from .stock import register_handlers_stock
from .sales import register_handlers_sales
from .finances import register_handlers_finances
from .notes import register_handlers_notes
from .settings import register_handlers_settings

def register_all_handlers(dp: Dispatcher):
    register_handlers_start(dp)
    register_handlers_stock(dp)
    register_handlers_sales(dp)
    register_handlers_finances(dp)
    register_handlers_notes(dp)
    register_handlers_settings(dp)
