import json
import requests
from datetime import datetime
from celery.utils.log import get_task_logger
from .models.employee_controller import EmployeeController

logger = get_task_logger(__name__)


class EmployeeTask:

    def __init__(self, config):
        self.config = config
        self.sqlalchemy_database_uri = self.config['SQLALCHEMY_DATABASE_URI']

    def action_with_hire_date(self):
        db_ctrl = EmployeeController(self.sqlalchemy_database_uri)
        try:
            offset = 0
            limit = 20
            select_date = datetime.today()
            list_employee = []
            while True:
                try:
                    # result = db_ctrl.get_employee_by_hire_date(select_date, offset, limit)
                    result = db_ctrl.get_employees_by_hire_date(select_date, offset, limit)
                except Exception as ex:
                    logger.warning(ex.__str__())
                    break
                if result:
                    list_employee.extend(result)
                    offset += limit
                else:
                    break
            return list_employee
        except Exception as ex:
            return ex.__str__()
        finally:
            db_ctrl.close()
