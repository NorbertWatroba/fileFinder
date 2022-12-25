from decouple import config
from pathlib import Path
from mysql.connector import connect, Error
from queries import *

root = config('ROOT')

host = config('HOST')
database = config('DATABASE')
user = config('USER')
password = config('PASSWORD')

conn = None
try:
    conn = connect(host=host, database=database, user=user, password=password)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute(create_categories_table)
        cursor.execute(create_files_table)
        cursor.execute(create_dependencies_table)
        print(f'MySQL Server Version {conn.get_server_info()}')
        for path in Path(root).rglob('*.jpg'):
            print(path)
            cursor.execute(insert_path(path))
        cursor.execute(r'INSERT INTO Files(path) VALUES("photos\Nowy folder\siege3.jpg")')
except Error as e:
    print(f'Error while connecting to the database: {e}')
finally:
    if conn:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print('MySQL connection closed')
