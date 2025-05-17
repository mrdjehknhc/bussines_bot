from aiogram import types, Dispatcher
from database import add_note, get_all_notes, delete_note

# /добавить_заметку
async def cmd_add_note(message: types.Message):
    await message.answer("📝 Введите текст заметки:")
    await NoteStates.waiting_for_note.set()

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class NoteStates(StatesGroup):
    waiting_for_note = State()

@NoteStates.waiting_for_note.handler()
async def process_note_text(message: types.Message, state: FSMContext):
    note_text = message.text
    add_note(note_text)
    await message.answer("✅ Заметка сохранена.")
    await state.finish()

# /заметки
async def cmd_show_notes(message: types.Message):
    notes = get_all_notes()
    if not notes:
        await message.answer("Заметок пока нет.")
        return

    text = "📒 <b>Заметки:</b>\n\n"
    for n in notes:
        text += f"🗒️ {n['text']} (ID: {n['id']})\n"
    text += "\nЧтобы удалить, напиши /удалить_заметку ID"

    await message.answer(text, parse_mode="HTML")

# /удалить_заметку
async def cmd_delete_note(message: types.Message):
    try:
        _, note_id = message.text.split()
        deleted = delete_note(int(note_id))
        if deleted:
            await message.answer("🗑️ Заметка удалена.")
        else:
            await message.answer("❌ Заметка с таким ID не найдена.")
    except:
        await message.answer("⚠️ Используй формат: /удалить_заметку ID")

def register_handlers_notes(dp: Dispatcher):
    dp.register_message_handler(cmd_add_note, commands=["добавить_заметку"])
    dp.register_message_handler(cmd_show_notes, commands=["заметки"])
    dp.register_message_handler(cmd_delete_note, commands=["удалить_заметку"])
    dp.register_message_handler(process_note_text, state=NoteStates.waiting_for_note)
