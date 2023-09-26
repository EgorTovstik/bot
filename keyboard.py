

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

main_kb = [
    [KeyboardButton(text='Выполнение запроса')]
    ]

main = ReplyKeyboardMarkup(keyboard=main_kb,
                           resize_keyboard=True,
                           input_field_placeholder='Нажмите кнопку для запуска программы')