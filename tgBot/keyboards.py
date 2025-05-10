from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Добавить задачу")],
            [KeyboardButton(text="📋 Просмотреть/Изменить задачи")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_task_list_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить задачу", callback_data="select_task")]
    ])

def get_task_actions_keyboard(task_idx, completed=False):
    complete_button_text = "Отметить невыполненной" if completed else "Отметить выполненной"
    complete_callback = f"uncomplete:{task_idx}" if completed else f"complete:{task_idx}"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete:{task_idx}")],
        [InlineKeyboardButton(text=complete_button_text, callback_data=complete_callback)],
        [InlineKeyboardButton(text="Изменить", callback_data=f"edit:{task_idx}")]
    ])

def get_edit_fields_keyboard(task_idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Название", callback_data=f"field:{task_idx}:title")],
        [InlineKeyboardButton(text="Описание", callback_data=f"field:{task_idx}:description")],
        [InlineKeyboardButton(text="Дедлайн", callback_data=f"field:{task_idx}:due_date")],
        [InlineKeyboardButton(text="Категории", callback_data=f"field:{task_idx}:categories")]
    ])
