from utils import sql_execute
from typing import Union
from pathlib import Path

@sql_execute()
def create_files_table():
    return r"""
CREATE TABLE Files(
Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
path varchar(260) NOT NULL UNIQUE)
"""

@sql_execute()
def create_categories_table():
    return r"""
CREATE TABLE Categories(
Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
Name varchar(15) NOT NULL UNIQUE)
"""

@sql_execute()
def create_dependencies_table():
    return r"""
CREATE TABLE Dependencies(
path_id int,
cat_id int,
FOREIGN KEY (path_id) REFERENCES Files(Id) ON DELETE CASCADE,
FOREIGN KEY (cat_id) REFERENCES Categories(Id) ON DELETE CASCADE)
"""

@sql_execute()
def insert_path(path: Union[str, Path]) -> str:
    formatted_path = str(path).replace('\\', '\\\\')
    return fr'INSERT INTO Files(path) VALUES("{formatted_path}")'


@sql_execute()
def get_all_paths() -> str:
    return r'SELECT Id, path FROM Files'


@sql_execute()
def get_all_categories() -> str:
    return r'SELECT Id, Name FROM Categories'


@sql_execute(lambda result: list(map(lambda row: row[0], result)))
def get_assigned_categories(file_id: int) -> str:
    return fr'SELECT cat_id FROM dependencies WHERE path_id = {file_id}'


@sql_execute()
def assign_category(file_id: int, category_id: int):
    return fr'INSERT INTO dependencies VALUES({file_id}, {category_id})'


@sql_execute()
def discharge_category(file_id: int, category_id: int):
    return fr'DELETE FROM dependencies WHERE path_id = {file_id} AND cat_id = {category_id}'


@sql_execute()
def create_category(category: str):
    return fr"INSERT INTO categories(`Name`) VALUES('{category.title()}')"

@sql_execute(lambda result: result[0][0])
def get_category_id(category_name: str):
    return fr'SELECT Id FROM Categories WHERE Name LIKE "{category_name}"'
