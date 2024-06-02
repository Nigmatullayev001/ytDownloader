from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def keylang():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.add(KeyboardButton('Русский 🇷🇺'), KeyboardButton('Oʻzbek 🇺🇿'), KeyboardButton('English 🇬🇧'))
    return rkm
