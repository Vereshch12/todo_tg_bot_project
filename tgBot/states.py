from aiogram.fsm.state import State, StatesGroup

class TaskManagement(StatesGroup):
    SELECT_TASK = State()
    TASK_ACTION = State()
    EDIT_FIELD = State()
    INPUT_NEW_VALUE = State()