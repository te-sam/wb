from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Одинокий пост")],
        [KeyboardButton(text="Групповой пост целиком")],
        [KeyboardButton(text="Групповой пост (только артикулы)")],
        # [KeyboardButton(text="📝 Заполнить анкету"), KeyboardButton(text="📚 Каталог")]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    
    return keyboard


def hastags_kb(user_telegram_id: int):
    kb_hash = [
        [KeyboardButton(text="#Одежда@go_wb_girl"), KeyboardButton(text="#Бельё@go_wb_girl")],
        [KeyboardButton(text="#Обувь@go_wb_girl"), KeyboardButton(text="#Украшения@go_wb_girl ")],
        [KeyboardButton(text="#Дом@go_wb_girl"), KeyboardButton(text="#Косметика@go_wb_girl")],
        [KeyboardButton(text="Без хэштега")],
    ]
    keyboard_hashtags = ReplyKeyboardMarkup(keyboard=kb_hash, resize_keyboard=True, one_time_keyboard=True)

    return keyboard_hashtags
