from configparser import ConfigParser
from mysql.connector import connect, Error


def read_config():
    config = ConfigParser()
    config.read('config.ini')
    return config

def sql_execute(formatting = None):
    def db_connection(func):
        def establish_connection(*args, **kwargs):
            config = read_config()
            host = config.get('DATABASE', 'HOST')
            database = config.get('DATABASE', 'DATABASE')
            user = config.get('DATABASE', 'USER')
            password = config.get('DATABASE', 'PASSWORD')
            try:
                conn = connect(host=host, database=database, user=user, password=password)
            except Error:
                raise Error

            with conn.cursor() as cursor:
                try:
                    cursor.execute(func(*args, **kwargs))
                    result = cursor.fetchall()
                    conn.commit()
                    if formatting:
                        result = formatting(result)
                    conn.close()
                    return result
                except Error as e:
                    print(f'Error: {e.msg}')
                    conn.close()
                    return 0

        return establish_connection
    return db_connection

def get_abs_path(path):
    config = read_config()
    root_path = config.get('OS', 'ABSOLUTE_PATH')
    return fr'{root_path}\{path}'

