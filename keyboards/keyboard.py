from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Одинокий пост")],
        [KeyboardButton(text="Групповой пост (целиком)")],
        [KeyboardButton(text="Групповой пост (только артикулы)")],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    
    return keyboard


def hastags_kb(user_telegram_id: int):
    kb_hash = [
        [KeyboardButton(text="#Одежда@go_wb_girl"), KeyboardButton(text="#Бельё@go_wb_girl")],
        [KeyboardButton(text="#Обувь@go_wb_girl"), KeyboardButton(text="#Украшения@go_wb_girl ")],
        [KeyboardButton(text="#Дом@go_wb_girl"), KeyboardButton(text="#Косметика@go_wb_girl")],
        [KeyboardButton(text="#Хобби@go_wb_girl"), KeyboardButton(text="Без хэштега")],
        [(KeyboardButton(text="Отмена"))]
    ]
    keyboard_hashtags = ReplyKeyboardMarkup(keyboard=kb_hash, resize_keyboard=True, one_time_keyboard=True)

    return keyboard_hashtags


def another_post_kb(user_telegram_id: int):
    kb_another = [
        [KeyboardButton(text="Сделать ещё пост😊")],
    ]
    keyboard_another = ReplyKeyboardMarkup(keyboard=kb_another, resize_keyboard=True, one_time_keyboard=True)

    return keyboard_another


def cancel_kb(user_telegram_id: int):
    kb_cancel = [
        [KeyboardButton(text="Отмена")],
    ]
    keyboard_cancel = ReplyKeyboardMarkup(keyboard=kb_cancel, resize_keyboard=True, one_time_keyboard=True)

    return keyboard_cancel



# def cancel_kb(user_telegram_id: int):
#     kb_cancel = [
#         [InlineKeyboardButton(text="Отмена", callback_data="quit")]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=kb_cancel)