import os
import sqlite3
import asyncio
import aiogram
import keyboard
from dotenv import load_dotenv
from keyboards.inline import *
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')
db = sqlite3.connect(DB_PATH)
c = db.cursor()
#c.execute("""CREATE TABLE info_user (
#          user_name text,
#          user_id integer)
#          """)
db.close()

def add_user(user_id):
    db = sqlite3.connect(DB_PATH)
    c = db.cursor()
    c.execute('SELECT user_id FROM info_user WHERE user_id = ?', (user_id,))
    if c.fetchone():
        return False
    db.close()

@dp.message(Command('start'))
async def start(message: Message):
    user_id = message.from_user.id
    if add_user(user_id) == False:
        await bot.send_message(chat_id=user_id, text='Узнал родной', reply_markup=lvl())
    else:
        await bot.send_message(chat_id=ADMIN_ID, text=f'Пользователь {message.from_user.first_name}, запрашивает доступ', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить', callback_data=f'allow:{message.from_user.id}'), InlineKeyboardButton(text='Отказать', callback_data=f'deny:{message.from_user.id}')]]))
    
@dp.message(Command('user'))
async def user(message:Message):
    if message.from_user.id == ADMIN_ID:
        await bot.send_message(chat_id=ADMIN_ID, text='Список пользователей:', reply_markup=users(DB_PATH))
    
@dp.callback_query()
async def handle_callback(callback_query: types.CallbackQuery):
    try:
        db = sqlite3.connect(DB_PATH)
        c = db.cursor()
        action, user_id = callback_query.data.split(":")  # Разделяем callback_data
        if action == 'allow':
            user_id = int(user_id)
            user_name = callback_query.message.text.split(' ')[1][:-1]
            c.execute('INSERT INTO info_user VALUES(?, ?)', (user_name, user_id))
            db.commit()
            await bot.send_message(chat_id=user_id, text='✅Вам одобрен доступ!')
        elif action == 'deny':
            await bot.send_message(chat_id=user_id, text='❌К сожалению доступ запрещен')
        db.close()
    except:
        db.close()
        option = callback_query.data
    if option == 'right':
        keyboard.press_and_release('right')
    elif option == 'left':
        keyboard.press_and_release('left')
    elif option == 'space':
        keyboard.press_and_release('space')
    elif option == 'off':
        keyboard.press_and_release('alt+f4')
    elif option == 'Enter':
        keyboard.press_and_release('enter')
    else:
        await bot.send_message(chat_id=ADMIN_ID, text=f'Пользователь {option}')
        test = delit_user(DB_PATH, option)
        if test:
            await bot.send_message(chat_id=ADMIN_ID, text=f'Пользователь {Message.text}')
        else:
            await bot.send_message(chat_id=ADMIN_ID, text=f'ПУ-ПУ-ПУ')


async def main():
    print('Запущен')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())