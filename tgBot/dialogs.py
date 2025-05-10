from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

class TaskDialog(StatesGroup):
    TITLE = State()
    DESCRIPTION = State()
    DUE_DATE = State()
    CATEGORIES = State()
    CONFIRM = State()

def get_task_dialog():
    from dialog_handlers import on_input_title, on_input_description, on_input_due_date, on_input_categories, on_confirm_clicked

    return Dialog(
        Window(
            Const("Введите название задачи:"),
            TextInput(id="title_input", on_success=on_input_title),
            state=TaskDialog.TITLE,
        ),
        Window(
            Const("Введите описание задачи:"),
            TextInput(id="description_input", on_success=on_input_description),
            state=TaskDialog.DESCRIPTION,
        ),
        Window(
            Const("Введите дедлайн задачи (ГГГГ-ММ-ДД ЧЧ:ММ, например, 2025-05-10 15:00):"),
            TextInput(id="due_date_input", on_success=on_input_due_date),
            state=TaskDialog.DUE_DATE,
        ),
        Window(
            Const("Введите категории (через запятую, например: Работа,Срочное):"),
            TextInput(id="categories_input", on_success=on_input_categories),
            state=TaskDialog.CATEGORIES,
        ),
        Window(
            Const("Подтвердить создание задачи?"),
            Button(Const("Да"), id="confirm", on_click=on_confirm_clicked),
            Button(Const("Отмена"), id="cancel", on_click=lambda c, b, m: m.done()),
            state=TaskDialog.CONFIRM,
        )
    )

task_dialog = get_task_dialog()