from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    telegram_id = message.from_user.id
    success = await link_telegram_id(telegram_id)
    await message.answer(
        f"{'Ваш аккаунт привязан!' if success else 'Ошибка привязки. Попробуйте позже.'} "
        "Используйте кнопки или /add_task, /show_tasks:",
        reply_markup=get_main_menu()
    )

async def display_tasks(message: Message, state: FSMContext):
    tasks = await get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("Нет задач. Добавьте через /add_task или 'Добавить задачу'!")
        return
    task_list = ["📋 <b>Задачи:</b>\n"]
    for idx, task in enumerate(tasks, 1):
        task_list.append(format_task(task, idx))
    await state.set_state(TaskManagement.SELECT_TASK)
    await state.update_data(tasks=tasks, message_id=message.message_id)
    await message.answer("\n".join(task_list), parse_mode="HTML", reply_markup=get_task_list_keyboard())

@router.message(lambda m: m.text in ["/add_task", "📝 Добавить задачу"])
async def add_task(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await state.clear()
    await dialog_manager.start(TaskDialog.TITLE, mode=StartMode.RESET_STACK)

@router.message(lambda m: m.text in ["/show_tasks", "📋 Просмотреть/Изменить задачи"])
async def show_tasks(message: Message, state: FSMContext):
    await display_tasks(message, state)

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.fsm.context import FSMContext

from api import link_telegram_id, get_tasks
from keyboards import get_main_menu, get_task_list_keyboard
from dialogs import TaskDialog
from states import TaskManagement
from utils import format_task

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    telegram_id = message.from_user.id
    success = await link_telegram_id(telegram_id)
    await message.answer(
        f"{'Ваш аккаунт привязан!' if success else 'Ошибка привязки. Попробуйте позже.'} "
        "Используйте кнопки или /add_task, /show_tasks:",
        reply_markup=get_main_menu()
    )

async def display_tasks(message: Message, state: FSMContext):
    tasks = await get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("Нет задач. Добавьте через /add_task или 'Добавить задачу'!")
        return
    task_list = ["📋 <b>Задачи:</b>\n"]
    for idx, task in enumerate(tasks, 1):
        task_list.append(format_task(task, idx))
    await state.set_state(TaskManagement.SELECT_TASK)
    await state.update_data(tasks=tasks, message_id=message.message_id)
    await message.answer("\n".join(task_list), parse_mode="HTML", reply_markup=get_task_list_keyboard())

@router.message(lambda m: m.text in ["/add_task", "📝 Добавить задачу"])
async def add_task(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await state.clear()
    await dialog_manager.start(TaskDialog.TITLE, mode=StartMode.RESET_STACK)

@router.message(lambda m: m.text in ["/show_tasks", "📋 Просмотреть/Изменить задачи"])
async def show_tasks(message: Message, state: FSMContext):
    await display_tasks(message, state)