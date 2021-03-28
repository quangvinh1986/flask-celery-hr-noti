import logging
from app.extensions import db
from app.database_connect.models import Regions
from app.libs.common.logger import TraceException
from app.libs.common.custom_exception import CustomControllerException, OK_MESSAGE

logger = logging.getLogger(__name__)


# <editor-fold desc="RegionController">
class RegionController:
    def get_by_id(self, _id):
        """
        :param _id:
        :return:
        """
        result = Regions.query.filter(Regions.REGION_ID == _id).first()
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
            trace = TraceException("RegionsController: add_or_update DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def add(self, args):
        """add new region
        :param args: dictionary for region params
        :return:
        """
        resend_case = Regions(**args)
        session = db.session()
        session.add(resend_case)
        try:
            session.commit()
            return OK_MESSAGE
        except Exception as e:
            trace = TraceException("RegionsController:", "insert DB fail", e.__str__())
            raise CustomControllerException(trace.get_message())
            # logger.warning(trace.get_message())
            # return {'error': trace.get_message(), 'status': "NOK"}

    def update(self, _id, args):
        """
        update by id
        :param
        :return:
        """
        db.session.query(Regions).filter_by(REGION_ID=_id).update(args)
        try:
            db.session.commit()
            return OK_MESSAGE
        except Exception as ex:
            trace = TraceException("RegionsController:", "update DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def delete(self, _id):
        obj = Regions.query.filter(Regions.REGION_ID == _id).first()
        if not obj:
            return OK_MESSAGE
        db.session.delete(obj)

        try:
            db.session.commit()
            return OK_MESSAGE
        except Exception as ex:
            db.session.rollback()
            trace = TraceException("RegionsController:", "delete DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def multi_delete(self, list_id):
        session = db.session()
        try:
            delete_q = Regions.__table__.delete().where(Regions.REGION_ID.in_(set(list_id)))
            session.execute(delete_q)
            session.commit()
            return OK_MESSAGE
        except Exception as ex:
            session.rollback()
            trace = TraceException("RegionsController: multi_delete " + ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_limit(self, limit):
        try:
            if limit:
                return db.session().query(Regions).order_by().limit(limit).all()
            else:
                return db.session().query(Regions).order_by().all()
        except Exception as ex:
            trace = TraceException("RegionsController:", "get_limit", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_all_case(self, region_name="", limit=0):
        if region_name:
            return self.get_by_region_name(region_name, limit)
        return self.get_limit(limit)

    def get_by_region_name(self, region_name, limit=0):
        try:
            if limit:
                return db.session().query(Regions).filter(Regions.REGION_NAME == region_name).order_by().limit(limit).all()
            else:
                return db.session().query(Regions).filter(Regions.REGION_NAME == region_name).order_by().all()
        except Exception as ex:
            trace = TraceException("RegionsController:", "get_by_region_name", ex.__str__())
            raise CustomControllerException(trace.get_message())

# </editor-fold>

