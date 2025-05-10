def format_task(task, idx=None):
    status = "Выполнена" if task["completed"] else "Не выполнена"
    categories = ", ".join(task["categories"]) or "Без категорий"
    prefix = f"<b>{idx}) " if idx else "<b>"
    return (
        f"{prefix}{task['title']}</b>\n"
        f"   Описание: {task['description']}\n"
        f"   Создано: {task['created_at']}\n"
        f"   Дедлайн: {task['due_date']}\n"
        f"   Категории: {categories}\n"
        f"   Статус: {status}\n\n"
    )