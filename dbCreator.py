# from pathlib import Path
from queries import *
from utils import read_config, db_connection
from mysql.connector import Error


@db_connection
def create_db(conn, cursor):
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


@db_connection
def fill_db(conn, cursor):
    config = read_config()
    root = config.get('OS', 'DIRECTORY')
    for path in Path(root).rglob('*.jpg'):
        try:
            cursor.execute(insert_path(path))
            conn.commit()
        except Error as e:
            print(f'Error while filling the database: {e.msg}')
    print('Finished filling!')


if __name__ == '__main__':
    fill_db()
