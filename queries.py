create_files_table = """
CREATE TABLE Files(
Id int NOT NULL AUTO INCREMENT PRIMARY KEY,
path varchar(250) NOT NULL DISTINCT)
"""

create_categories_table = """
CREATE TABLE Categories(
Id int NOT NULL AUTO INCREMENT PRIMARY KEY,
Name varchar(15) NOT NULL DISTINCT)
"""


def insert_path(path):
    query = f'INSERT IGNORE INTO Files(path) VALUES("{path}")'
    return query
