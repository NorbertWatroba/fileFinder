from configparser import ConfigParser
from pathlib import Path
from mysql.connector import connect, Error
from queries import *


def read_config():
    config = ConfigParser()
    config.read('config.ini')
    return config


def establish_connection():
    config = read_config()
    host = config.get('DATABASE', 'HOST')
    database = config.get('DATABASE', 'DATABASE')
    user = config.get('DATABASE', 'USER')
    password = config.get('DATABASE', 'PASSWORD')
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
        print('Database creation successful!')
        cursor.close()
        conn.close()
        fill_db()


def fill_db():
    try:
        config = read_config()
        root = config.get('OS', 'ROOT')
        conn, cursor = establish_connection()
        for path in Path(root).rglob('*.jpg'):
            cursor.execute(insert_path(path))
        conn.commit()
    except Error as e:
        print(f'Error while filling the database: {e}')
    finally:
        print('Filling successful!')

'''
root = config.get('OS', 'ROOT')
host = config.get('DATABASE', 'HOST')
database = config.get('DATABASE', 'DATABASE')
user = config.get('DATABASE', 'USER')
password = config.get('DATABASE', 'PASSWORD')
print(host, database, user, password, root)
'''