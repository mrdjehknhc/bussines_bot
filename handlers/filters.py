# Пример фильтра (если понадобится позже)
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in [123456789]  # ID администратора
