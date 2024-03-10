import mysql.connector
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from datetime import date, datetime, time
import keyboards as kb
from config import host, user, password, database, ADMINS
from scheduler import bot

router = Router()


def connect_to_database():
    return mysql.connector.connect(host=host, user=user,
                                   password=password, database=database)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Assalomu alaykum! Xududingizni tanlang:", reply_markup=await kb.inline_regions())


@router.message(F.text == "Bugungi vaqtlarni olish")
async def get_today_timings(message: Message):
    # Получаем дату сегодня
    today_date = date.today()

    # Получаем регион пользователя из базы данных
    user_id = message.from_user.id
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT region FROM users WHERE user_id = %s", (user_id,))
    region_row = cursor.fetchone()
    if region_row:
        region = region_row[0]
    else:
        await message.answer("Siz hali hududingizni tanlamagansiz. Hududingizni tanlang:")
        return

    # Выполняем запрос к базе данных для получения данных о времени за сегодня для данного региона
    cursor.execute("SELECT * FROM trial WHERE region = %s AND date = %s", (region, today_date))
    timings_rows = cursor.fetchall()
    cursor.close()
    connection.close()

    # Отправляем данные пользователю
    if timings_rows:
        response_message = "Bugungi vaqtlar:\n"
        for row in timings_rows:
            response_message += (f"<b>Xudud:</b> {row[1]},\n"
                                 f"<b>Sana:</b> {row[5]},\n"
                                 f"<b>Hijriy sana:</b> {row[7]} {row[6]} 1445 yil,\n"
                                 f"<b>Hafta kuni:</b> {row[8]},\n"
                                 f"<b>Tong/saharlik:</b> {row[9]},\n"
                                 f"<b>Quyosh:</b> {row[10]},\n"
                                 f"<b>Peshin:</b> {row[11]},\n"
                                 f"<b>Asr:</b> {row[12]},\n"
                                 f"<b>Shom/iftor:</b> {row[13]},\n"
                                 f"<b>Hufton:</b> {row[14]}\n\n")
        await message.answer(response_message, parse_mode='HTML')
    else:
        await message.answer("Bugun uchun ma'lumot topilmadi.")


@router.message(F.text == "Xududni o\'zgartirish")
async def change_region(message: Message):
    await message.answer("Xududni o\'zgartirish:", reply_markup=await kb.inline_regions())


@router.callback_query(lambda callback: F.data == callback.data)
async def choosen_region(callback: CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    region = callback.data

    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute("UPDATE users SET region = %s WHERE user_id = %s", (region, user_id))
        connection.commit()
        await callback.message.answer(f'Hududingizni {callback.data}ga o\'zgartirildi')
    else:
        cursor.execute("INSERT INTO users (user_id, first_name, region) VALUES (%s, %s, %s)",
                       (user_id, first_name, region))
        connection.commit()
        await callback.message.answer(f'Hududingiz belgilandi - {callback.data}')

    # Закрыть инлайн клавиатуру
    await callback.message.edit_reply_markup(reply_markup=None)
    # Скрыть приветственное сообщение
    await callback.message.delete()

    await callback.message.answer("Xududni o'zgartirish va bugungi kungi taqvimni pastgi tugmalar orqali olishingiz "
                                  "mumkin", reply_markup=kb.keyboard)

    cursor.close()
    connection.close()


@router.message(F.from_user.id == ADMINS)
async def admin_message_handler(message: Message):
    # Retrieve all user IDs from the database
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users")
    user_ids = cursor.fetchall()
    cursor.close()
    connection.close()

    # Send the message to all users
    for user_id in user_ids:
        try:
            await bot.send_message(user_id[0], message.text)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")


@router.message(F.text == "Vaqtni tekshirish")
async def check_time(message: Message):
    # Получаем текущее время и часовой пояс
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_timezone = time.tzname[0]

    # Отправляем данные пользователю
    response_message = f"Serverdagi vaqt: {current_time}\n"
    response_message += f"Soat mintaqasi: {current_timezone}"
    await message.answer(response_message)
