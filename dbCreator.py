from decouple import config
from pathlib import Path
from mysql.connector import connect, Error
from queries import *


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
        conn.commit()

    except Error as e:
        print(f'Error while connecting to the database: {e}')
    finally:
        cursor.close()
        conn.close()
        fill_db()


def fill_db():
    try:
        root = config('ROOT')
        conn, cursor = establish_connection()
        for path in Path(root).rglob('*.jpg'):
            cursor.execute(insert_path(path))
        conn.commit()
    except Error as e:
        print(f'Error while filling the database: {e}')
    finally:
        print('Filling successful!')
