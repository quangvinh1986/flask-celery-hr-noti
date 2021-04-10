from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker


class DBConnection(object):

    def __init__(self, connection_string):
        self.db = create_engine(connection_string)
        self.meta = MetaData(self.db)
        Session = sessionmaker(bind=self.db)
        self.session = Session()
