from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
import keyboards as kb
import mysql.connector
from config import host, user, password, database

router = Router()


def connect_to_database():
    return mysql.connector.connect(host=host, user=user,
                                   password=password, database=database)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Assalomu alaykum! Xududingizni tanlang:", reply_markup=await kb.inline_regions())


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

    cursor.close()
    connection.close()

