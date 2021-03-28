from app.extensions import db
from datetime import datetime


class MethodsMixin(object):
    """
    This class mixes in some common Class table functions like
    delete and save
    """

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete(self):
        ret = self.id
        db.session.delete(self)
        db.session.commit()
        return ret

    def update(self):
        ret = db.session.commit()
        return ret


class Regions(db.Model, MethodsMixin):
    __tablename__ = "REGIONS"
    REGION_ID = db.Column(db.Integer, primary_key=True)
    REGION_NAME = db.Column(db.String)

    def __init__(self, **kwargs):
        keys = ['REGION_NAME']
        for key in keys:
            setattr(self, key, kwargs.get(key, ""))

    def set_value(self, dict_value):
        keys = ['REGION_NAME']
        for key in keys:
            setattr(self, key, dict_value.get(key, ""))

    def __str__(self):
        return '{}-{}'.format(self.REGION_ID, self.REGION_NAME)

    def get_json_serializeable(self):
        """Return object data in easily serializeable format"""
        dict_value = {
            'regionId': str(self.REGION_ID),
            'regionName': self.REGION_NAME
        }
        return dict_value


class Countries(db.Model, MethodsMixin):
    __tablename__ = "COUNTRIES"
    COUNTRY_ID = db.Column(db.String, primary_key=True)
    COUNTRY_NAME = db.Column(db.String)
    REGION_ID = db.Column(db.String)

    def __init__(self, **kwargs):
        keys = ['COUNTRY_ID', 'COUNTRY_NAME', 'REGION_ID']
        for key in keys:
            setattr(self, key, kwargs.get(key, ""))

    def set_value(self, dict_value):
        keys = ['COUNTRY_ID', 'COUNTRY_NAME', 'REGION_ID']
        for key in keys:
            setattr(self, key, dict_value.get(key, ""))

    def __str__(self):
        return '{}-{}-{}'.format(self.COUNTRY_ID, self.COUNTRY_NAME, self.REGION_ID)

    def get_json_serializeable(self):
        """Return object data in easily serializeable format"""
        dict_value = {
            'countryId': self.COUNTRY_ID,
            'countryName': self.COUNTRY_NAME,
            'regionId': self.REGION_ID
        }
        return dict_value


class Locations(db.Model, MethodsMixin):
    __tablename__ = "LOCATIONS"
    LOCATION_ID = db.Column(db.Integer, primary_key=True)
    STREET_ADDRESS = db.Column(db.String)
    POSTAL_CODE = db.Column(db.String)
    CITY = db.Column(db.String)
    STATE_PROVINCE = db.Column(db.String)
    COUNTRY_ID = db.Column(db.String)

    def __init__(self, **kwargs):
        keys = ['STREET_ADDRESS', 'POSTAL_CODE', 'CITY', 'STATE_PROVINCE', 'COUNTRY_ID']
        for key in keys:
            setattr(self, key, kwargs.get(key, ""))

    def set_value(self, dict_value):
        keys = ['STREET_ADDRESS', 'POSTAL_CODE', 'CITY', 'STATE_PROVINCE', 'COUNTRY_ID']
        for key in keys:
            setattr(self, key, dict_value.get(key, ""))

    def __str__(self):
        return str(self.__dict__)

    def get_json_serializeable(self):
        """Return object data in easily serializeable format"""
        item_dict = self.__dict__
        item_dict.pop('_sa_instance_state')

        return item_dict


class Departments(db.Model, MethodsMixin):
    __tablename__ = "DEPARTMENTS"
    DEPARTMENT_ID = db.Column(db.Integer, primary_key=True)
    DEPARTMENT_NAME = db.Column(db.String)
    MANAGER_ID = db.Column(db.Integer)
    LOCATION_ID = db.Column(db.Integer)

    def __init__(self, **kwargs):
        keys = ['DEPARTMENT_NAME', 'MANAGER_ID', 'LOCATION_ID']
        for key in keys:
            setattr(self, key, kwargs.get(key, ""))

    def set_value(self, dict_value):
        keys = ['DEPARTMENT_NAME', 'MANAGER_ID', 'LOCATION_ID']
        for key in keys:
            setattr(self, key, dict_value.get(key, ""))

    def __str__(self):
        return str(self.__dict__)

    def get_json_serializeable(self):
        """Return object data in easily serializeable format"""
        item_dict = self.__dict__
        item_dict.pop('_sa_instance_state')
        return item_dict


class Employees(db.Model, MethodsMixin):
    __tablename__ = "EMPLOYEES"
    EMPLOYEE_ID = db.Column(db.Integer, primary_key=True)
    FIRST_NAME = db.Column(db.String)
    LAST_NAME = db.Column(db.String)
    EMAIL = db.Column(db.String)
    PHONE_NUMBER = db.Column(db.String)
    HIRE_DATE = db.Column(db.DateTime)
    JOB_ID = db.Column(db.String)
    SALARY = db.Column(db.Integer)
    COMMISSION_PCT = db.Column(db.Float)
    MANAGER_ID = db.Column(db.Integer)
    DEPARTMENT_ID = db.Column(db.Integer)

    def __init__(self, **kwargs):
        keys = ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'PHONE_NUMBER', 'HIRE_DATE', 'JOB_ID', 'SALARY', 'COMMISSION_PCT',
                'MANAGER_ID', 'DEPARTMENT_ID']
        for key in keys:
            setattr(self, key, kwargs.get(key, ""))

    def set_value(self, dict_value):
        keys = ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'PHONE_NUMBER', 'HIRE_DATE', 'JOB_ID', 'SALARY', 'COMMISSION_PCT',
                'MANAGER_ID', 'DEPARTMENT_ID']
        for key in keys:
            setattr(self, key, dict_value.get(key, ""))

    def __str__(self):
        return str(self.__dict__)

    def get_json_serializeable(self):
        """Return object data in easily serializeable format"""
        item_dict = self.__dict__
        item_dict.pop('_sa_instance_state')
        return item_dict


class Jobs(db.Model, MethodsMixin):
    __tablename__ = "JOBS"
    JOB_ID = db.Column(db.String, primary_key=True)
    JOB_TITLE = db.Column(db.String)
    MIN_SALARY = db.Column(db.Integer)
    MAX_SALARY = db.Column(db.Integer)

    def __init__(self, **kwargs):
        keys = ['JOB_ID', 'JOB_TITLE', 'MIN_SALARY', 'MAX_SALARY']
        for key in keys:
            setattr(self, key, kwargs.get(key, ""))

    def set_value(self, dict_value):
        keys = ['JOB_ID', 'JOB_TITLE', 'MIN_SALARY', 'MAX_SALARY']
        for key in keys:
            setattr(self, key, dict_value.get(key, ""))

    def __str__(self):
        return str(self.__dict__)

    def get_json_serializeable(self):
        """Return object data in easily serializeable format"""
        item_dict = self.__dict__
        item_dict.pop('_sa_instance_state')
        return item_dict


class JobHistory(db.Model, MethodsMixin):
    __tablename__ = "JOB_HISTORY"
    EMPLOYEE_ID = db.Column(db.Integer, primary_key=True)
    START_DATE = db.Column(db.DateTime, primary_key=True)
    END_DATE = db.Column(db.DateTime)
    JOB_ID = db.Column(db.String)
    DEPARTMENT_ID = db.Column(db.Integer)

    def __init__(self, **kwargs):
        keys = ['EMPLOYEE_ID', 'START_DATE', 'END_DATE', 'JOB_ID', 'DEPARTMENT_ID']
        for key in keys:
            setattr(self, key, kwargs.get(key, ""))

    def set_value(self, dict_value):
        keys = ['EMPLOYEE_ID', 'START_DATE', 'END_DATE', 'JOB_ID', 'DEPARTMENT_ID']
        for key in keys:
            setattr(self, key, dict_value.get(key, ""))

    def __str__(self):
        return str(self.__dict__)

    def get_json_serializeable(self):
        """Return object data in easily serializeable format"""
        item_dict = self.__dict__
        item_dict.pop('_sa_instance_state')
        return item_dict
