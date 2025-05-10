from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from api import link_telegram_id, get_tasks
from dialogs import task_dialog, TaskDialog

router = Router()

# Клавиатура с кнопками
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Добавить задачу")],
            [KeyboardButton(text="📋 Просмотреть задачи")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

# Обработчик /start
@router.message(Command("start"))
async def start_command(message: Message):
    telegram_id = message.from_user.id
    success = await link_telegram_id(telegram_id)
    await message.answer(
        f"{'Ваш аккаунт привязан!' if success else 'Ошибка привязки. Попробуйте позже.'} "
        "Используйте кнопки или /add_task, /show_tasks:",
        reply_markup=get_main_menu()
    )

# Общая логика для отображения задач
async def display_tasks(message: Message):
    tasks = await get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("Нет задач. Добавьте через /add_task или 'Добавить задачу'!")
        return
    task_list = ["📋 <b>Задачи:</b>\n"]
    for idx, task in enumerate(tasks, 1):
        status = "Выполнена" if task["completed"] else "Не выполнена"
        categories = ", ".join(task["categories"]) or "Без категорий"
        task_list.append(
            f"<b>{idx}) {task['title']}</b>\n"
            f"Описание: {task['description']}\n"
            f"Создано: {task['created_at']}\n"
            f"Дедлайн: {task['due_date']}\n"
            f"Категории: {categories}\n"
            f"Статус: {status}\n\n"
        )
    await message.answer("\n".join(task_list), parse_mode="HTML")

# Обработчик для добавления задачи (команда и кнопка)
@router.message(lambda m: m.text in ["/add_task", "📝 Добавить задачу"])
async def add_task(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(TaskDialog.TITLE, mode=StartMode.RESET_STACK)

# Обработчик для просмотра задач (команда и кнопка)
@router.message(lambda m: m.text in ["/show_tasks", "📋 Просмотреть задачи"])
async def show_tasks(message: Message):
    await display_tasks(message)

def setup_handlers(dp):
    dp.include_router(router)
    dp.include_router(task_dialog)