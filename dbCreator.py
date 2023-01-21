from pathlib import Path
from queries import create_categories_table, create_files_table, create_dependencies_table, insert_path
from utils import read_config, sql_execute
from mysql.connector import Error


def create_db():
    create_categories_table()
    create_files_table()
    create_dependencies_table()
    fill_db()


@sql_execute()
def fill_db():
    config = read_config()
    root = config.get('OS', 'DIRECTORY')
    query = 'INSERT INTO Files(path) VALUES'
    values = []
    for path in Path(root).rglob('*.jpg'):
        formatted_path = str(path).replace('\\', '\\\\')
        packed_path = fr'("{formatted_path}")'
        values.append(packed_path)

    values = ', '.join(values)
    query += values
    return query


def fill_db2():
    config = read_config()
    root = config.get('OS', 'DIRECTORY')
    for path in Path(root).rglob('*.jpg'):
        try:
            insert_path(path)
        except Error as e:
            print(e.msg)


if __name__ == '__main__':
    create_db()
