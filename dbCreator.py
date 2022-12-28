from decouple import config
from pathlib import Path
from mysql.connector import connect, Error
from queries import *

root = config('ROOT')


def establish_connection():
    host = config('HOST')
    database = config('DATABASE')
    user = config('USER')
    password = config('PASSWORD')
    try:
        conn = connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        return conn, cursor
    except Error:
        raise Error


def create_db():
    conn, cursor = establish_connection()
    try:
        cursor.execute(create_categories_table)
        cursor.execute(create_files_table)
        cursor.execute(create_dependencies_table)
        fill_db()
    except Error as e:
        print(f'Error while connecting to the database: {e}')
    finally:
        if conn:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print('MySQL connection closed')


def fill_db():
    conn, cursor = establish_connection()
    try:
        for path in Path(root).rglob('*.jpg'):
            print(path)
            cursor.execute(insert_path(path))
    except Error as e:
        print(f'Error while filling the database: {e}')
    finally:
        print('Filling successful!')


host = config('HOST')
database = config('DATABASE')
user = config('USER')
password = config('PASSWORD')
try:
    conn = connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
except Error:
    raise Error
