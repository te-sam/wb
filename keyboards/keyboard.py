from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Одинокий пост"), KeyboardButton(text="Групповой пост")],
        # [KeyboardButton(text="📝 Заполнить анкету"), KeyboardButton(text="📚 Каталог")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard