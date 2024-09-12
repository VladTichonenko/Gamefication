import asyncio
from reaktion import reaction
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import keyboard as krb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config as cf
#from Gamefication import database as db
from database import DataBase
import os
from datetime import datetime, timedelta
from collections import defaultdict
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import requests
import time

BOT_TOKEN='7106909032:AAHSN6OOHppekDf4_pwxqBffVw-vWfsQmxw'


# функция на добовления плохих слов
def load_bad_words(url):
    response = requests.get(url)
    # Проверка на успешный ответ
    if response.status_code == 200:
        # Разбиваем текст на строки и возвращаем список слов
        return response.text.splitlines()
    else:
        print(f"Не удалось загрузить файл. Статус код: {response.status_code}")
        return []


# Константы
POINTS_PER_COMMENT = 1
MAX_COMMENTS_PER_DAY = 3

user_data = defaultdict(lambda: {'points': 0, 'comments': 0, 'last_comment_time': datetime.now()})
# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурация бота
bot = Bot(token='7106909032:AAHSN6OOHppekDf4_pwxqBffVw-vWfsQmxw')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

user_scores = {}

# Список плохих слов
# URL с плохими словами
bad_words_url = "https://www.cs.cmu.edu/~biglou/resources/bad-words.txt"

# Загружаем плохие слова
bad_words = load_bad_words(bad_words_url)

# ID канала, который нужно проверить
Chanel_id="-1002208916163"
Chanel2_id="-1002154835852"
Not_Sub_Message="Для доступа к функционалу, пожалуйста подпишитесь на канал!"
storage=MemoryStorage()

db1 = DataBase(r'E:/gemivication/Gamefication/database/users.db')

async def check_subscriptions(user_id, channel_ids):
    subscriptions = []
    for channel_id in channel_ids:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        subscriptions.append(chek_chanel(member))
    return all(subscriptions)
# константы


async def on_startup(_):
    
    print('Бот успешно запущен!')

# Классы для FSM
class NewOrder(StatesGroup):
    name=State()
    price=State()
    photo=State()

class CancelOrder(StatesGroup):
    cancel = State()


# проверка на подписку
def chek_chanel(chat_member):
    # print(chat_member['status'])
    if chat_member['status']!='left':
        return True
    else:
        return False
def creater(chat_member):
    if chat_member['status']=="creator":
        return True
    else:
        return False


# хэндлеры
# Хэндлер для команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global user_id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    full_name = f'{user_name} {user_last_name}' if user_last_name else user_name

    chat_member = await bot.get_chat_member(chat_id=Chanel_id, user_id=message.from_user.id)
    if chek_chanel(chat_member):
        if not db1.user_exists(message.from_user.id):
            start_command = message.text
            referer_id = str(start_command[7:])  # Предполагается, что ссылка начинается с '/start '
            if referer_id != "":
                if referer_id != str(message.from_user.id):
                    db1.add_user(message.from_user.id, referer_id)
                    await bot.send_message(referer_id, "По вашей ссылке зарегистрировался новый пользователь")
                else:
                    db1.add_user(message.from_user.id)
                    await bot.send_message(message.from_user.id, "Нельзя регистрировать по собственной реферальной ссылке!")
            else:
                db1.add_user(message.from_user.id)
        await message.answer(f'Привет, {full_name}\nДобро пожаловать в TGplay!', reply_markup=krb.create_keyboard(user_id))
    else:
        await bot.send_message(message.from_user.id, Not_Sub_Message, reply_markup=krb.My_Chanel)

@dp.message_handler(commands=['admin'])
async def start(message: types.Message):
    print(1)
    if creater(await bot.get_chat_member(chat_id=Chanel_id, user_id=message.from_user.id)):
        await message.answer("Успешный вход в админ панель✅")
        await message.answer("Чтобы добавить приз нажмите на сит фразу /admin_1_get_users\nЧтобы вернуться в меню /start")
    else:
        await message.answer("Вы не являетесь владельцем канала(")

@dp.message_handler(commands=['admin_1_get_users'])
async def start(message: types.Message):
    await message.answer("Давайте добавим приз!\nВведите название ", reply_markup=krb.cancel_keyboard())
    await NewOrder.next()

# Создание или подключение к базе данных
"""
def setup_database():
    conn = sqlite3.connect('Gamefication/database/users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  referal_id INTEGER NOT NULL,
  points INTEGER DEFAULT 0
);
    ''')
    #conn.commit()
    #return conn

def get_user_score(conn, user_id):
    c = conn.cursor()
    c.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    return result[0] if result else 0

def update_user_score(conn, user_id, points):
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (user_id, referer_id, points) VALUES (?, NULL, ?)
        ON CONFLICT(user_id) DO UPDATE SET points = points + excluded.points
    ''', (user_id, points))
    conn.commit()
"""

# Вызов функции для настройки базы данных
# db_connection = setup_database()

# Словарь для отслеживания комментариев пользователей
user_comments = defaultdict(list)


# !!!!!!!!
# Хэндлер для обработки комментариев и сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    full_name = f'{user_name} {user_last_name}' if user_last_name else user_name

    if message.chat.type == 'supergroup':
        user_id = message.from_user.id
        message_text = message.text.lower()

        # Получаем текущее количество баллов пользователя
        current_score = db1.get_user_score(user_id)
        if current_score is None:
            current_score = 0

        # Проверяем время и количество комментариев
        current_time = time.time()  # Текущее время в секундах с момента начала эпохи
        user_comments[user_id] = [timestamp for timestamp in user_comments[user_id] if
                                  current_time - timestamp <= 5 * 3600]  # Оставляем только комментарии за последние 5 часов

        if len(user_comments[user_id]) < 3:
            # Начисляем балл, если комментариев меньше 3 за 5 часов
            db1.update_user_score(user_id, 1)
            current_score += 1
            user_comments[user_id].append(current_time)  # Добавляем текущее время в список

            await message.answer(f'{full_name}, Ваши баллы: {current_score}')
        else:
            # Если пользователь достиг лимита, предупреждаем его
            await message.answer(
                f'{full_name}, вы достигли лимита в 3 комментария за 5 часов. Остальные комментарии не будут начислены баллы.')

        # Проверяем на наличие плохих слов
        if message_text in (".", "плохо", "xxx" , "ХУЙ"):
            # current_score -= 1
            await message.delete()  # Удаляем плохое сообщение
            await message.answer(
                f'{full_name}, в Вашем комментарии обнаружено негативное слово!\nСообщение было удалено. Ваши баллы: {current_score}')





@dp.message_handler(state=NewOrder.name)
async def start(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['name']=message.text
    await message.answer("Введите количество баллов за приз", reply_markup=krb.cancel_keyboard())
    await NewOrder.next()

@dp.message_handler(state=NewOrder.price)
async def start(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['price']=message.text
    await message.answer("Отправьте фото", reply_markup=krb.cancel_keyboard())
    await NewOrder.next()

@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    # Получаем фото и выбираем наибольшее качество
    photo = message.photo[-1]  # берём самое качественное фото (последний элемент)
    # Получаем файл изображения
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    # Указываем путь для сохранения
    way = '/GAmefication/img/' + file.file_path.split('/')[
        -1]  # Добавляем имя файла
    # Скачиваем файл
    await bot.download_file(file.file_path, way)  # Сохраняем файл
    print("Фото сохранено")
    # Сохраняем идентификатор файла в состоянии
    async with state.proxy() as data:
        data['photo'] = file_id
    # Добавляем элемент в базу данных
    await db1.add_item(state)
    await message.answer('Приз успешно добавлен!')
    await state.finish()


@dp.callback_query_handler(text='cancel', state="*")
async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.answer("Добавление отменено.")
    await callback_query.message.answer (f'Добро пожаловать в TGplay!', reply_markup=krb.create_keyboard(user_id))





# калбэки
@dp.callback_query_handler(text="sub")
async def subchanel(callback_query: types.CallbackQuery):
    user_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    full_name = f'{user_name} {user_last_name}' if user_last_name else user_name
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    if chek_chanel(await bot.get_chat_member(chat_id=Chanel_id, user_id=callback_query.from_user.id)):
        await bot.send_message(callback_query.from_user.id, f'Привет, {full_name}\nДобро пожаловать в TGplay!', reply_markup=krb.create_keyboard(user_id))
    else:
        await bot.send_message(callback_query.from_user.id, Not_Sub_Message, reply_markup=krb.My_Chanel)



@dp.callback_query_handler(lambda query: query.data == 'more')
async def More(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        "<b>TGplay: Получайте больше от подписки на канал!</b>\n\n"
        "Проявляйте активность, выполняйте дополнительные задания, "
        "копите очки и разблокируйте награды!🎁\n\n"
        "️️⚠️ Награды, их содержание и доставка являются ответственностью админов/владельцев каналов.",
        parse_mode='HTML'  # Указываем режим разметки
    )


# реферальная система
@dp.callback_query_handler(lambda query: query.data == 'profile')
async def Prof(callback_query: types.CallbackQuery):
    if callback_query.message.chat.type == 'private':
        user_name = callback_query.from_user.first_name
        user_last_name = callback_query.from_user.last_name
        user_id = callback_query.from_user.id
        referals_count = db1.count_referals(user_id)  # предполагается, что функция принимает user_id
        full_name = f'{user_name} {user_last_name}' if user_last_name else user_name
        await bot.send_message(callback_query.from_user.id, f'👤 {full_name}\n\nВаш ID: {callback_query.from_user.id}\nВаша реферальная ссылка 🎁: https://t.me/{cf.BOT_NAME}?start={callback_query.from_user.id}\n\nКол-во рефералов: {referals_count}')

@dp.message_handler(content_types=types.ContentType.ANY)
async def add_button_to_new_post(message: types.Message):
    if message.chat.type == 'channel':
        keyboard = InlineKeyboardMarkup()
        participate_button = InlineKeyboardButton('Участвовать', callback_data='participate')
        keyboard.add(participate_button)

        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

@dp.channel_post_handler()
async def channel_message(message: types.Message):
    # Когда в канале появляется новое сообщение, оно будет обрабатываться здесь
    reactions = await reaction()
    db1.update_user_score(db1.get_random_user_id,reactions*50)
    print(f"Saving to DB")

@dp.channel_post_handler()
async def channel_message(message: types.Message):
    # Создаем кнопку с ссылкой на пост
    post_url = f"впиши сюда ссылку на канал"
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("Перейти к посту", url=post_url))

    # Отправляем сообщение с кнопкой в бота
    await bot.send_message(message.chat.id, "Новый пост в канале!", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('reaction'))
async def process_callback_reaction(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    initial_reactions = await reaction()

    await asyncio.sleep(10)  # Ждем 10 секунд

    final_reactions = await reaction()

    if final_reactions > initial_reactions:
        points = final_reactions - initial_reactions
        db1.update_user_score(user_id, points)
        await bot.answer_callback_query(callback_query.id, f"Вы получили {points} баллов!")
    else:
        await bot.answer_callback_query(callback_query.id, "Количество реакций не изменилось.")


if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    except:
        pass
