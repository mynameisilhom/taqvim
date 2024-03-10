# import time
# from datetime import datetime, timedelta
#
# import mysql.connector
# from mysql.connector import Error
#
# from config import host, database, user, password
#
#
# def connect_to_mysql():
#     try:
#         connection = mysql.connector.connect(
#             host=host,
#             database=database,
#             user=user,
#             password=password
#         )
#         if connection.is_connected():
#             print("Connected to MySQL database")
#             return connection
#     except Error as e:
#         print(f"Error while connecting to MySQL: {e}")
#         return None
#
#
# def get_time_columns(connection, table_name):
#     time_columns = []
#     try:
#         cursor = connection.cursor()
#         cursor.execute(f"SHOW COLUMNS FROM {table_name} WHERE Type LIKE 'time%'")
#         rows = cursor.fetchall()
#         for row in rows:
#             time_columns.append(row[0])
#         cursor.close()
#     except Error as e:
#         print(f"Error while fetching time columns: {e}")
#     return time_columns
#
#
# def check_time_columns_and_send_text(connection, table_name, time_columns):
#     try:
#         cursor = connection.cursor()
#         columns_str = ', '.join(time_columns)
#         cursor.execute(f"SELECT {columns_str} FROM {table_name}")
#         rows = cursor.fetchall()
#         current_time = datetime.now()
#         send_time = current_time + timedelta(minutes=30)
#         # current_time_str = current_time.strftime("%H:%M")
#         send_time_str = send_time.strftime("%H:%M")
#         # print(f"Current time: {current_time_str}, Send time: {send_time_str}")
#         for i, row in enumerate(rows):
#             for j, time_value in enumerate(row):
#                 # Создаем объекты datetime из timedelta
#                 time_obj = datetime.min + time_value
#                 time_value_str = time_obj.strftime("%H:%M")
#                 # print(f"Time value from database: {time_value_str}")
#                 if send_time_str == time_value_str:
#                     print(f"Bugungi {time_columns[j]} vaqtiga: {time_value}")
#         cursor.close()
#     except Error as e:
#         print(f"Error while fetching data from MySQL: {e}")
#
#
# def main():
#     connection = connect_to_mysql()
#     if connection:
#         table_name = "text"  # Название вашей таблицы
#         time_columns = get_time_columns(connection, table_name)
#         while True:
#             check_time_columns_and_send_text(connection, table_name, time_columns)
#             # Проверяем столбцы каждые 60 секунд
#             time.sleep(60)
#
#
# if __name__ == "__main__":
#     main()
