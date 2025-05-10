import logging
from aiogram_dialog import DialogManager
from aiogram.types import Message
from aiogram_dialog.widgets.input import ManagedTextInput
from api import create_task
from dialogs import TaskDialog
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

async def save_task(data: dict, dialog_manager: DialogManager):
    telegram_id = dialog_manager.event.from_user.id
    categories = data.get("categories", "").split(",")
    categories = [cat.strip() for cat in categories if cat.strip()]
    task_data = {
        "title": data["title"],
        "description": data["description"],
        "due_date": data["due_date"],
        "categories": categories
    }
    logger.info(f"Attempting to create task: {task_data}")
    success = await create_task(telegram_id, task_data)
    if success:
        await dialog_manager.event.answer("Задача успешно создана!")
    else:
        await dialog_manager.event.answer("Не удалось создать задачу. Попробуйте позже.")
    await dialog_manager.done()

async def on_input_title(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str):
    logger.info(f"Received title input: {value}")
    if not value.strip():
        await message.answer("Название задачи не может быть пустым! Пожалуйста, введите название.")
        return
    dialog_manager.dialog_data["title"] = value.strip()
    await message.answer("Название сохранено. Переходим к следующему шагу...")
    await dialog_manager.switch_to(TaskDialog.DESCRIPTION)

async def on_input_description(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str):
    logger.info(f"Received description input: {value}")
    if not value.strip():
        await message.answer("Описание задачи не может быть пустым! Пожалуйста, введите описание.")
        return
    dialog_manager.dialog_data["description"] = value.strip()
    await message.answer("Описание сохранено. Переходим к следующему шагу...")
    await dialog_manager.switch_to(TaskDialog.DUE_DATE)

async def on_input_due_date(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str):
    logger.info(f"Received due_date input: {value}")
    if not value.strip():
        await message.answer("Дедлайн не может быть пустым! Пожалуйста, введите дедлайн в формате ГГГГ-ММ-ДД ЧЧ:ММ.")
        return
    try:
        parsed_date = datetime.strptime(value.strip(), "%Y-%m-%d %H:%M")
        adak_tz = ZoneInfo("America/Adak")
        parsed_date = parsed_date.replace(tzinfo=adak_tz)
        dialog_manager.dialog_data["due_date"] = parsed_date.isoformat()
    except ValueError:
        await message.answer("Неверный формат даты! Пожалуйста, используйте ГГГГ-ММ-ДД ЧЧ:ММ (например, 2025-05-10 15:00).")
        return
    await message.answer("Дедлайн сохранён. Переходим к следующему шагу...")
    await dialog_manager.switch_to(TaskDialog.CATEGORIES)

async def on_input_categories(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str):
    logger.info(f"Received categories input: {value}")
    if not value.strip():
        await message.answer("Категории не могут быть пустыми! Пожалуйста, введите хотя бы одну категорию (через запятую).")
        return
    dialog_manager.dialog_data["categories"] = value.strip()
    await message.answer("Категории сохранены. Переходим к подтверждению...")
    await dialog_manager.switch_to(TaskDialog.CONFIRM)

async def on_confirm_clicked(callback, button, dialog_manager: DialogManager):
    logger.info("Confirm button clicked")
    await save_task(dialog_manager.dialog_data, dialog_manager)