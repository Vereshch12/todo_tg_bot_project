from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from api import link_telegram_id, get_tasks
from dialogs import task_dialog, TaskDialog

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    telegram_id = message.from_user.id
    success = await link_telegram_id(telegram_id)
    if success:
        await message.answer("Ваш аккаунт успешно привязан!")
    else:
        await message.answer("Не удалось привязать аккаунт. Попробуйте позже.")

@router.message(Command("add_task"))
async def add_task_command(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(TaskDialog.TITLE, mode=StartMode.RESET_STACK)

@router.message(Command("show_tasks"))
async def show_tasks_command(message: Message):
    telegram_id = message.from_user.id
    tasks = await get_tasks(telegram_id)
    if not tasks:
        await message.answer("У вас нет задач. Создайте новую с помощью /add_task!")
        return

    task_list = ["📋 <b>Ваши задачи:</b>\n"]
    for idx, task in enumerate(tasks, 1):
        status = "Выполнена" if task["completed"] else "Не выполнена"
        categories = ", ".join(task["categories"]) if task["categories"] else "Без категорий"
        task_text = (
            f"<b>{idx}) {task['title']}</b>\n"
            f"  Описание: {task['description']}\n"
            f"  Создано: {task['created_at']}\n"
            f"  Дедлайн: {task['due_date']}\n"
            f"  Категории: {categories}\n"
            f"  Статус: {status}\n\n"
        )
        task_list.append(task_text)

    await message.answer("\n".join(task_list), parse_mode="HTML")

def setup_handlers(dp):
    dp.include_router(router)
    dp.include_router(task_dialog)