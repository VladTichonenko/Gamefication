from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import keyboard as krb
import config as cf
from GAmefication import database as db
from database import DataBase
import os
storage=MemoryStorage()

db1=DataBase('bonus.db')

bot = Bot(token='7106909032:AAHSN6OOHppekDf4_pwxqBffVw-vWfsQmxw')
dp = Dispatcher(bot, storage=storage)

# константы
Chanel_id="-1002208916163"
Not_Sub_Message="Для доступа к функционалу, пожалуйста подпишитесь на канал!"
async def on_startup(_):
    await db.db_start()
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
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    full_name = f'{user_name} {user_last_name}' if user_last_name else user_name
    if chek_chanel(await bot.get_chat_member(chat_id=Chanel_id , user_id=message.from_user.id)):
        if not db1.user_exists(message.from_user.id):
            print(1)
            start_comand=message.text
            referer_id=str(start_comand[7:])
            if str(referer_id)!="":
                print(2)
                if str(referer_id) != str(message.from_user.id):
                    db1.add_user(message.from_user.id, referer_id)
                    print(referer_id)
                    try:
                        await bot.send_message(referer_id, "По вашей ссылке зарегистрировался новый пользователь")
                    except Exception as ex:
                        print(ex)
                else:
                    db1.add_user(message.from_user.id)
                    await bot.send_message(message.from_user.id, "Нельзя регистрировать по собственной реферальной ссылке!")
            else:
                db1.add_user(message.from_user.id)
        await message.answer(f'Привет, {full_name}\nДобро пожаловать в ......', reply_markup=krb.glav)

    else:
        await bot.send_message(message.from_user.id, Not_Sub_Message , reply_markup=krb.My_Chanel)

@dp.message_handler(commands=['admin_1_get_users'])
async def start(message: types.Message):

    await message.answer("Давайте добавим приз!\nВведите название ", reply_markup=krb.cancel_keyboard())
    await NewOrder.next()

@dp.message_handler(state=NewOrder.name)
async def start(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['name']=message.text
    await message.answer("Введите количество баллов за приз", reply_markup=krb.cancel_keyboard())
    await NewOrder.next()

@dp.message_handler(state=NewOrder.price)
async def start(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['price']=message.photo[0].file_id
    await message.answer("Отправьте фото", reply_markup=krb.cancel_keyboard())
    await NewOrder.next()

@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')

@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Приз успешно добавлен!')
    await state.finish()

@dp.callback_query_handler(text='cancel', state="*")
async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.answer("Добавление отменено.")
    await callback_query.message.answer (f'Добро пожаловать в ......', reply_markup=krb.glav)

@dp.message_handler(commands=['admin'])
async def start(message: types.Message):
    if creater(await bot.get_chat_member(chat_id=Chanel_id, user_id=message.from_user.id)):
        await message.answer("Успешный вход в админ панель✅")
        await message.answer("Чтобы добавить приз нажмите на сит фразу /admin_1_get_users\nЧтобы вернуться в меню /start")
    else:
        await message.answer("Вы не являетесь владельцем канала(")



# калбэки
@dp.callback_query_handler(text="sub")
async def subchanel(callback_query: types.CallbackQuery):
    user_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    full_name = f'{user_name} {user_last_name}' if user_last_name else user_name
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    if chek_chanel(await bot.get_chat_member(chat_id=Chanel_id, user_id=callback_query.from_user.id)):
        await bot.send_message(callback_query.from_user.id, f'Привет, {full_name}\nДобро пожаловать в ......', reply_markup=krb.glav)
    else:
        await bot.send_message(callback_query.from_user.id, Not_Sub_Message, reply_markup=krb.My_Chanel)


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

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)