import logging
from app.extensions import db
from app.database_connect.models import Countries
from app.libs.common.logger import TraceException
from app.libs.common.custom_exception import CustomControllerException, OK_MESSAGE

logger = logging.getLogger(__name__)


# <editor-fold desc="CountryController">
class CountryController:
    def get_by_id(self, _id):
        """
        :param _id:
        :return:
        """
        result = Countries.query.filter(Countries.COUNTRY_ID == _id).first()
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
            trace = TraceException("CountriesController: add_or_update DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def add(self, args):
        """add new countries
        :param args: dictionary for countries
        :return:
        """
        resend_case = Countries(**args)
        session = db.session()
        session.add(resend_case)
        try:
            session.commit()
            return OK_MESSAGE
        except Exception as e:
            trace = TraceException("CountriesController:", "insert DB fail", e.__str__())
            raise CustomControllerException(trace.get_message())

    def update(self, _id, args):
        """update
        :param
        :return:
        """
        db.session.query(Countries).filter_by(COUNTRY_ID=_id).update(args)
        try:
            db.session.commit()
            return OK_MESSAGE
        except Exception as ex:
            trace = TraceException("CountriesController:", "update DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def delete(self, _id):
        obj = Countries.query.filter(Countries.COUNTRY_ID == _id).first()
        if not obj:
            return OK_MESSAGE
        db.session.delete(obj)

        try:
            db.session.commit()
            return OK_MESSAGE
        except Exception as ex:
            db.session.rollback()
            trace = TraceException("CountriesController:", "delete DB fail", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def multi_delete(self, list_id):
        session = db.session()
        try:
            delete_q = Countries.__table__.delete().where(Countries.COUNTRY_ID.in_(set(list_id)))
            session.execute(delete_q)
            session.commit()
            return OK_MESSAGE
        except Exception as ex:
            session.rollback()
            trace = TraceException("CountriesController: multi_delete " + ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_limit(self, limit):
        try:
            if limit:
                return db.session().query(Countries).order_by().limit(limit).all()
            else:
                return db.session().query(Countries).order_by().all()
        except Exception as ex:
            trace = TraceException("CountriesController:", "get_limit", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_all_case(self, limit=0):
        return self.get_limit(limit)

    def get_by_region_id(self, region_id, limit=0):
        try:
            if limit:
                return db.session().query(Countries).filter(Countries.REGION_ID == region_id).order_by().limit(limit).all()
            else:
                return db.session().query(Countries).filter(Countries.REGION_ID == region_id).order_by().all()
        except Exception as ex:
            trace = TraceException("CountriesController:", "get_by_region_id", ex.__str__())
            raise CustomControllerException(trace.get_message())

    def get_like_country_name(self, country_name, limit=0):
        try:
            if limit:
                return db.session().query(Countries).filter(Countries.COUNTRY_NAME.like("%" + country_name + "%"))\
                    .limit(limit).all()
            else:
                return db.session().query(Countries).filter(Countries.COUNTRY_NAME.like("%" + country_name + "%")).all()
        except Exception as ex:
            trace = TraceException("CountriesController:", "get_like_country_name", ex.__str__())
            raise CustomControllerException(trace.get_message())
# </editor-fold>

