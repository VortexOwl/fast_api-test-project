from sqlite3 import connect
from sys import exc_info
import asyncio

from logs import log_debug, log_error


# ----------------------------------------------------------------------------------------------------------------------
# Подключаемся к БД и вытаскиваем из таблицы incidents все записи
# ----------------------------------------------------------------------------------------------------------------------
async def get_records() -> list:
    log_debug("Устанавливаем соединение с БД.")
    try:
        with connect('databases/places.sqlite') as connection:
            log_debug("Соединение с БД установлено.")
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(
                """Create table if Not Exists incidents (
                        id integer primary key AUTOINCREMENT,
                        description text not null,
                        status integer not null,
                        source text not null,
                        date_create date)""")
            records = cursor.execute("""select * from incidents""").fetchall()
            return records
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        log_error(message=e, module_name=exc_tb.tb_frame.f_code.co_filename.split('/')[-1], line_no=exc_tb.tb_lineno)


# ----------------------------------------------------------------------------------------------------------------------
# Подключаемся к БД и вытаскиваем из таблицы incidents все записи с указанным статусом
# ----------------------------------------------------------------------------------------------------------------------
async def search_records_by_status(status: int) -> list:
    log_debug("Устанавливаем соединение с БД.")
    try:
        with connect('databases/places.sqlite') as connection:
            log_debug("Соединение с БД установлено.")
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(
                """Create table if Not Exists incidents (
                        id integer primary key AUTOINCREMENT,
                        description text not null,
                        status integer not null,
                        source text not null,
                        date_create date)""")
            records = cursor.execute("""select * from incidents where status=?""", (status,)).fetchall()
            return records
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        log_error(message=e, module_name=exc_tb.tb_frame.f_code.co_filename.split('/')[-1], line_no=exc_tb.tb_lineno)


# ----------------------------------------------------------------------------------------------------------------------
# Подключаемся к БД и добавляем в таблицу incidents новую запись
# ----------------------------------------------------------------------------------------------------------------------
async def create_record(description:str, status:int, source:str, date:str):
    log_debug("Устанавливаем соединение с БД.")
    try:
        with connect('databases/places.sqlite') as connection:
            log_debug("Соединение с БД установлено.")
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(
                """Create table if Not Exists incidents (
                        id integer primary key AUTOINCREMENT,
                        description text not null,
                        status integer not null,
                        source text not null,
                        date_create date)""")
            cursor.execute("""Insert into incidents(description, status, source, date_create) Values(?, ?, ?, ?)""", (description, status, source, date))
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        log_error(message=e, module_name=exc_tb.tb_frame.f_code.co_filename.split('/')[-1], line_no=exc_tb.tb_lineno)
        

# ----------------------------------------------------------------------------------------------------------------------
# Подключаемся к БД и изменяем в таблице incidents статус записи с указанным id 
# ----------------------------------------------------------------------------------------------------------------------
async def change_record_status_by_id(id_record: int, status: int) -> bool:
    log_debug("Устанавливаем соединение с БД.")
    try:
        with connect('databases/places.sqlite') as connection:
            log_debug("Соединение с БД установлено.")
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(
                """Create table if Not Exists incidents (
                        id integer primary key AUTOINCREMENT,
                        description text not null,
                        status integer not null,
                        source text not null,
                        date_create date)""")
            record = cursor.execute("""select * from incidents where id=?""", (id_record,)).fetchone()
            if record:
                cursor.execute("""Update incidents Set status=? where id=?""", (status, id_record,))
                return True
            return False
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        log_error(message=e, module_name=exc_tb.tb_frame.f_code.co_filename.split('/')[-1], line_no=exc_tb.tb_lineno)
