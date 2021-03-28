import os
from pathlib import Path

_database_folder = "database"
_database_name = "HR_sqlite.db"
DATABASE_PATH = os.path.join(Path(os.path.abspath(os.path.dirname(__file__))).parent, _database_folder, _database_name)
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE_PATH)
