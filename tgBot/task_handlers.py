from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from datetime import datetime
from zoneinfo import ZoneInfo
from states import TaskManagement
from api import delete_task, complete_task, uncomplete_task, update_task
from keyboards import get_task_actions_keyboard, get_edit_fields_keyboard
from utils import format_task

router = Router()

@router.callback_query(TaskManagement.SELECT_TASK, lambda c: c.data == "select_task")
async def select_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tasks = data.get("tasks", [])
    if not tasks:
        await callback.message.answer("Задачи не найдены!")
        await callback.answer()
        return
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Введите номер задачи:")
    await callback.answer()

@router.message(TaskManagement.SELECT_TASK)
async def process_task_number(message: Message, state: FSMContext):
    try:
        task_idx = int(message.text.strip()) - 1
        data = await state.get_data()
        tasks = data.get("tasks", [])
        if task_idx < 0 or task_idx >= len(tasks):
            await message.answer("Неверный номер задачи! Попробуйте снова.")
            return
        task = tasks[task_idx]
        await state.set_state(TaskManagement.TASK_ACTION)
        await state.update_data(task_idx=task_idx)
        await message.answer(format_task(task), parse_mode="HTML",
                             reply_markup=get_task_actions_keyboard(task_idx, task["completed"]))
    except ValueError:
        await message.answer("Пожалуйста, введите число!")

@router.callback_query(TaskManagement.TASK_ACTION, lambda c: c.data.startswith(("delete:", "complete:", "uncomplete:")))
async def task_action(callback: CallbackQuery, state: FSMContext):
    action, task_idx = callback.data.split(":")
    task_idx = int(task_idx)
    data = await state.get_data()
    tasks = data.get("tasks", [])
    if task_idx >= len(tasks):
        await callback.message.answer("Задача не найдена!")
        await callback.answer()
        return
    task_id = tasks[task_idx]["id"]
    await callback.message.edit_reply_markup(reply_markup=None)

    if action == "delete":
        success = await delete_task(task_id)
        await callback.message.answer("Задача удалена!" if success else "Ошибка при удалении!")
    elif action == "complete":
        success = await complete_task(task_id)
        await callback.message.answer("Задача отмечена выполненной!" if success else "Ошибка при отметке!")
    elif action == "uncomplete":
        success = await uncomplete_task(task_id)
        await callback.message.answer("Задача отмечена невыполненной!" if success else "Ошибка при отметке!")

    await callback.answer()

@router.callback_query(TaskManagement.TASK_ACTION, lambda c: c.data.startswith("edit:"))
async def edit_task_action(callback: CallbackQuery, state: FSMContext):
    task_idx = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(TaskManagement.EDIT_FIELD)
    await state.update_data(task_idx=task_idx)
    await callback.message.answer("Выберите, что вы хотите изменить:",
                                  reply_markup=get_edit_fields_keyboard(task_idx))
    await callback.answer()

@router.callback_query(TaskManagement.EDIT_FIELD, lambda c: c.data.startswith("field:"))
async def select_edit_field(callback: CallbackQuery, state: FSMContext):
    _, task_idx, field = callback.data.split(":")
    task_idx = int(task_idx)
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(TaskManagement.INPUT_NEW_VALUE)
    await state.update_data(field=field)
    prompts = {
        "title": "Введите новое название задачи:",
        "description": "Введите новое описание задачи:",
        "due_date": "Введите новый дедлайн (ГГГГ-ММ-ДД ЧЧ:ММ):",
        "categories": "Введите новые категории (через запятую):"
    }
    await callback.message.answer(prompts[field])
    await callback.answer()

@router.message(TaskManagement.INPUT_NEW_VALUE)
async def input_new_value(message: Message, state: FSMContext):
    data = await state.get_data()
    task_idx = data.get("task_idx")
    field = data.get("field")
    tasks = data.get("tasks", [])
    if task_idx >= len(tasks):
        await message.answer("Задача не найдена!")
        await state.clear()
        return
    task_id = tasks[task_idx]["id"]
    value = message.text.strip()

    if field == "due_date":
        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d %H:%M")
            adak_tz = ZoneInfo("America/Adak")
            value = parsed_date.replace(tzinfo=adak_tz).isoformat()
        except ValueError:
            await message.answer("Неверный формат даты! Используйте ГГГГ-ММ-ДД ЧЧ:ММ.")
            return

    update_data = {field: value}
    if field == "categories":
        update_data[field] = [cat.strip() for cat in value.split(",") if cat.strip()]

    success = await update_task(message.from_user.id, task_id, update_data)
    await message.answer("Задача обновлена!" if success else "Ошибка при обновлении!")
    await state.clear()
