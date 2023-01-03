from utils import db_connection
from typing import Union, List
from pathlib import Path


create_files_table = """
CREATE TABLE Files(
Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
path varchar(260) NOT NULL UNIQUE)
"""

create_categories_table = """
CREATE TABLE Categories(
Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
Name varchar(15) NOT NULL UNIQUE)
"""

create_dependencies_table = """
CREATE TABLE Dependencies(
path_id int,
cat_id int,
FOREIGN KEY (path_id) REFERENCES Files(Id) ON DELETE CASCADE,
FOREIGN KEY (cat_id) REFERENCES Categories(Id) ON DELETE CASCADE)
"""


def insert_path(path: Union[str, Path]) -> str:
    formatted_path = str(path).replace('\\', '\\\\')
    query = fr'INSERT INTO Files(path) VALUES("{formatted_path}")'
    return query


@db_connection
def get_all_paths(conn, cursor) -> List[tuple]:
    cursor.execute('SELECT Id, path FROM Files')
    result = cursor.fetchall()
    return result


@db_connection
def get_all_categories(conn, cursor) -> List[tuple]:
    cursor.execute('SELECT Id, Name FROM Categories')
    result = cursor.fetchall()
    return result


@db_connection
def get_assigned_categories(file: int, conn, cursor) -> List[int]:
    cursor.execute(f'SELECT cat_id FROM dependencies WHERE path_id = {file}')
    result = cursor.fetchall()
    categories = list(map(lambda x: x[0], result))
    return categories


@db_connection
def assign_category(file: int, category: int, conn, cursor):
    cursor.execute(f'INSERT INTO dependencies VALUES({file}, {category})')
    conn.commit()


@db_connection
def discharge_category(file: int, category: int, conn, cursor):
    cursor.execute(f'DELETE FROM dependencies WHERE path_id = {file} AND cat_id = {category}')
    conn.commit()


@db_connection
def create_category(category: str, conn, cursor):
    cursor.execute(f"INSERT INTO categories(`Name`) VALUES('{category.title()}')")
    conn.commit()
