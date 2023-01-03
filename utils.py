from configparser import ConfigParser
from mysql.connector import connect, Error


def read_config():
    config = ConfigParser()
    config.read('config.ini')
    return config


def db_connection(func):
    def establish_connection(*args, **kwargs):
        config = read_config()
        host = config.get('DATABASE', 'HOST')
        database = config.get('DATABASE', 'DATABASE')
        user = config.get('DATABASE', 'USER')
        password = config.get('DATABASE', 'PASSWORD')
        try:
            conn = connect(host=host, database=database, user=user, password=password)
            cursor = conn.cursor()
            result = func(*args, **kwargs, conn=conn, cursor=cursor)
            cursor.close()
            conn.close()
        except Error:
            raise Error
        return result
    return establish_connection


def size_scaling(img_size: tuple, wdw_size: tuple):
    img_x, img_y = img_size
    wdw_x, wdw_y = wdw_size
    cell_x = wdw_x / 3 - 20
    cell_y = (wdw_y-65) / 2 - 20
    resize = min(cell_x / img_x, cell_y / img_y)
    final_size = (img_x * resize, img_y * resize)
    return final_size


def get_abs_path(path):
    config = read_config()
    root_path = config.get('OS', 'ABSOLUTE_PATH')
    return fr'{root_path}\{path}'

