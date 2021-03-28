import logging
from app.extensions import db
from app.database_connect.models import Locations
from app.libs.common.logger import TraceException
from app.libs.common.custom_exception import CustomControllerException, OK_MESSAGE

logger = logging.getLogger(__name__)


# <editor-fold desc="LocationController">
class LocationController:
    def get_by_id(self, _id):
        """
        :param _id:
        :return:
        """
        result = Locations.query.filter(Locations.LOCATION_ID == _id).first()
        if result:
            return result.get_json_serializeable()
        else:
            return None

    def add_or_update(self, params, _id=""):
        """add new if don't exist
            update if exist
        :param _id: id of record
        :param params: dictionary
        :return: content is dictionary {"content":"...."}
        """
        try:
            if _id and self.get_by_id(_id):
                return self.update(_id, params)
            else:
                return self.add(params)
        except Exception as ex:
            db.session.rollback()
            trace = TraceException("LocationController: add_or_update DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def add(self, args):
        """add new bank deposit
        :param args: dictionary for bankdeposit
        :return:
        """
        params = Locations(**args)
        session = db.session()
        session.add(params)
        try:
            session.commit()
            return OK_MESSAGE
        except Exception as e:
            trace = TraceException("LocationController:", "insert DB fail", e.__str__())
            raise CustomControllerException(trace.get_message())

    def update(self, _id, args):
        """
        update
        :param
        :return:
        """
        db.session.query(Locations).filter_by(LOCATION_ID=_id).update(args)
        try:
            db.session.commit()
            return OK_MESSAGE
        except Exception as ex:
            trace = TraceException("LocationController:", "update DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def delete(self, _id):
        obj = Locations.query.filter(Locations.LOCATION_ID == _id).first()
        if not obj:
            return OK_MESSAGE
        db.session.delete(obj)

        try:
            db.session.commit()
            return OK_MESSAGE
        except Exception as ex:
            db.session.rollback()
            trace = TraceException("LocationController:", "delete DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def multi_delete(self, list_id):
        session = db.session()
        try:
            delete_q = Locations.__table__.delete().where(Locations.LOCATION_ID.in_(set(list_id)))
            session.execute(delete_q)
            session.commit()
            return OK_MESSAGE
        except Exception as ex:
            session.rollback()
            trace = TraceException("LocationController: multi_delete " + ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_limit(self, limit):
        try:
            if limit:
                return db.session().query(Locations).order_by().limit(limit).all()
            else:
                return db.session().query(Locations).order_by().all()
        except Exception as ex:
            trace = TraceException("LocationController:", "get_limit", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_all_case(self, city_name="", limit=0):
        if city_name:
            return self.get_by_city(city_name, limit)
        return self.get_limit(limit)

    def get_by_city(self, city_name, limit=0):
        try:
            if limit:
                return db.session().query(Locations).filter(Locations.CITY == city_name).order_by().limit(limit).all()
            else:
                return db.session().query(Locations).filter(Locations.CITY == city_name).order_by().all()
        except Exception as ex:
            trace = TraceException("LocationController:", "get_by_city", ex.__str__())
            raise CustomControllerException(trace.get_message())
# </editor-fold>

