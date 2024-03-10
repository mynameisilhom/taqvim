import asyncio
from datetime import datetime, timedelta

import mysql.connector
from aiogram import Bot, Dispatcher
from mysql.connector import Error

from config import TOKEN, host, database, user, password

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Функция для подключения к базе данных MySQL
async def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            print("Подключение к базе данных MySQL выполнено успешно")
            return connection
    except Error as e:
        print(f"Ошибка при подключении к MySQL: {e}")
        return None


# Функция для получения столбцов с временем из базы данных
async def get_time_columns(connection, table_name):
    time_columns = []
    try:
        cursor = connection.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {table_name} WHERE Type LIKE 'time%'")
        rows = cursor.fetchall()
        for row in rows:
            time_columns.append(row[0])
        cursor.close()
        print("Столбцы с временем успешно получены")
    except Error as e:
        print(f"Ошибка при получении столбцов с временем: {e}")
    return time_columns


# Функция для проверки столбцов с временем и отправки текста
async def check_time_columns_and_send_text(connection, table_name, time_columns):
    try:
        cursor = connection.cursor()
        columns_str = ', '.join(time_columns)
        today = datetime.now().date()
        cursor.execute(f"SELECT region, {columns_str} FROM {table_name} WHERE date = %s", (today,))
        rows = cursor.fetchall()
        current_time = datetime.now()
        send_time = current_time + timedelta(minutes=30)
        send_time_str = send_time.strftime("%H:%M")
        sent_messages = set()
        for row in rows:
            region = row[0]
            for j, time_value in enumerate(row[1:]):
                time_obj = datetime.min + time_value
                time_value_str = time_obj.strftime("%H:%M")
                message_key = (region, time_columns[j], today)
                if message_key in sent_messages:
                    continue
                if send_time_str == time_value_str:
                    message_text = f"Bugungi {time_columns[j]} vaqti {region}da: {time_value}"
                    await send_message_to_users(message_text, region, table_name, today)
                    sent_messages.add(message_key)
        cursor.close()
        print("Данные успешно получены и обработаны")
    except Error as e:
        print(f"Ошибка при получении данных из MySQL: {e}")


# Функция для отправки сообщений пользователям
async def send_message_to_users(message_text, region, table_name, today):
    try:
        connection = await connect_to_mysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT u.user_id FROM users u JOIN {table_name} t ON u.region = t.region WHERE t.region = %s AND t.date = %s",
                (region, today))
            user_ids = cursor.fetchall()
            for user_id in user_ids:
                print(f"Отправка сообщения пользователю {user_id[0]}: {message_text}")  # Отладочное сообщение
                with open('sent_messages.log', 'a') as file:
                    file.write(
                        f"Регион: {region}, ID пользователя: {user_id[0]}, Сообщение: {message_text}\n")  # Запись в 
                    # файл
                await bot.send_message(chat_id=user_id[0], text=message_text)
            cursor.close()
            connection.close()  # Закрываем соединение после отправки сообщений
            print("Сообщения успешно отправлены")
    except Error as e:
        print(f"Ошибка при получении ID пользователей из MySQL: {e}")


# Основная функция программы
async def main():
    connection = await connect_to_mysql()
    if connection:
        table_name = "trial"
        time_columns = await get_time_columns(connection, table_name)
        while True:
            await check_time_columns_and_send_text(connection, table_name, time_columns)
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
