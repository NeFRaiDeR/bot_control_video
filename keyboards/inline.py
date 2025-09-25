import os
import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def lvl():
    callback=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Пауза/Запуск', callback_data='space')],
                                                    [InlineKeyboardButton(text='Назад', callback_data='left'),
                                                    InlineKeyboardButton(text='Вперед', callback_data='right')], 
                                                    [InlineKeyboardButton(text='alt+f4', callback_data='off')],
                                                    [InlineKeyboardButton(text='Enter', callback_data='Enter')]])
    return callback

def users(DB_PATH):
    db = sqlite3.connect(DB_PATH)
    c = db.cursor()
    c.execute("SELECT * FROM info_user")
    from_users = c.fetchall()
    db.close()
    keyboard_buttons = []
    for i in from_users:
        keyboard_buttons.append([InlineKeyboardButton(text=i[0], callback_data=str(i[1]))])
    callback = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return callback    

def delit_user(db_path, user_id):
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM info_user WHERE user_id = ?", (user_id,))
        db.commit()

        if c.rowcount > 0:
            return True
        else:
            return False
    sqlite3.connect(db_path).close()