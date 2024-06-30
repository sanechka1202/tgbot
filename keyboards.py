
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рейтинг фильма')],
                                     [KeyboardButton(text='Рейтинг фильмов режиссера')],
                                     [KeyboardButton(text='Рейтинг фильмов актёра/актрисы')],
                                     ],
                           resize_keyboard=True,
                           input_field_placeholder='Что хотите найти?')
