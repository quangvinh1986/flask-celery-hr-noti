import os
from pathlib import Path

_database_folder = "database"
_database_name = "HR_sqlite.db"
DATABASE_PATH = os.path.join(Path(os.path.abspath(os.path.dirname(__file__))).parent, _database_folder, _database_name)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE_PATH)

# [PRIVATE information]
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://admin:2341312@127.0.0.1:5432/HR"
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20

EMAIL_SENDER = "vinh.nguyenquang@vinh.com.vn"
EMAIL_SENDER_PASSWORD = "*****"
EMAIL_SERVER_SMTP = "0.0.0.0"
EMAIL_SERVER_PORT = 25

