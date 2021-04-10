from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, String, MetaData, Integer, DateTime, Float, and_, func, extract
from . import DBConnection


class EmployeeController(DBConnection):

    def __init__(self, connection_string):
        DBConnection.__init__(self, connection_string)
        self.Employee = self.get_table()
        self.connection = self.db.connect()

    def get_table(self):
        table = Table('EMPLOYEES', self.meta,
                      Column('EMPLOYEE_ID', Integer, primary_key=True),
                      Column('FIRST_NAME', String),
                      Column('LAST_NAME', String),
                      Column('EMAIL', String),
                      Column('PHONE_NUMBER', String),
                      Column('HIRE_DATE', DateTime),
                      Column('JOB_ID', String),
                      Column('SALARY', Integer),
                      Column('COMMISSION_PCT', Float),
                      Column('MANAGER_ID', Integer),
                      Column('DEPARTMENT_ID', Integer),
                      autoload=True, autoload_with=self.db
                      )
        return table

    def close(self):
        self.session.close()
        self.connection.close()

    def get_all_record(self, offset=0, limit=20):
        value = self.session.query(self.Employee).offset(offset).limit(limit)
        result = value.all()
        return result

    def get_employee_by_hire_date(self, hire_date, offset=0, limit=20):
        # date_compare = datetime.strptime("2020-06-17", "%Y-%m-%d")
        value = self.session.query(self.Employee)\
            .filter(extract('month', self.Employee.c.HIRE_DATE) == hire_date.month)\
            .filter(extract('day', self.Employee.c.HIRE_DATE) == hire_date.day)\
            .offset(offset).limit(limit)
        result = value.all()
        return result
