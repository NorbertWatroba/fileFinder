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


def insert_path(path) -> str:
    query = f'INSERT INTO Files(path) VALUES("{path}")'
    return query
