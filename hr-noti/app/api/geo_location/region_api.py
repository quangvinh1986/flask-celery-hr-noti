from flask import current_app
from werkzeug.exceptions import NotFound
from app.libs.schema import geo_location_schema
from flask_restplus_patched import Resource
from app.extensions import api
from app.libs.common.logger import TraceException
from app.libs.common.custom_exception import CustomControllerException, ERROR_MESSAGE
from app.database_connect import regions_model


ns = api.namespace("geoLocation")


@ns.route("/regions")
class RegionsAPI(Resource):
    @ns.parameters(geo_location_schema.RegionsGetAllParams())
    def get(self, args):
        """
        get all regions
        :param args:
        :return:
        """
        try:
            limit = args.get("limit", 0)
            region_name = args.get("regionName", "")
            regions = regions_model.get_all_case(region_name, limit)
            lst_resgions = []
            for region in regions:
                lst_resgions.append(region.get_json_serializeable())
            if lst_resgions:
                return lst_resgions, 200
            else:
                return [], 404
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return {'error': trace.get_message(), 'status': "FAIL"}, 500

    @ns.parameters(geo_location_schema.RegionsPostParams(), locations=('json',))
    def post(self, args):
        """
        create new region with input params
        :param args:
        :return:
        """
        try:
            data = dict()
            data['REGION_NAME'] = args.get('regionName', "")
            result = regions_model.add(data)
            return result, 200
        except CustomControllerException as ex:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("update or add", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return {'error': trace.get_message(), 'status': "FAIL"}, 500

    @ns.parameters(geo_location_schema.RegionsDeleteParams(), locations=('json',))
    def delete(self, args):
        """
        delete multi record.
        :param args:
        :return:
        """
        try:
            list_id = args.get('listId', [])
            result = regions_model.multi_delete(list_id)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("multi delete", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE


@ns.route("/region/<regionId>")
class RegionsAPI(Resource):
    @ns.parameters(geo_location_schema.BlankParams())
    def get(self, args, **kwargs):
        """
        get single region by regionId
        :param args:
        :param kwargs:
        :return:
        """
        try:
            region_id = kwargs.get("regionId", 0)
            if not region_id:
                raise NotFound("Không có dữ liệu regionId")
            region = regions_model.get_by_id(region_id)
            return region, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("get_region_by_id fail", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500

    @ns.parameters(geo_location_schema.RegionsPostParams(), locations=('json',))
    def put(self, args, **kwargs):
        """
        Update region by regionId
        :param args:
        :param kwargs:
        :return:
        """
        try:
            data = dict()
            region_id = kwargs.get("regionId", 0)
            if not region_id:
                raise NotFound("Không có dữ liệu regionId")
            data['REGION_NAME'] = args.get('regionName', "")
            result = regions_model.update(data, region_id)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("update or add", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500

    @ns.parameters(geo_location_schema.BlankParams())
    def delete(self, args, **kwargs):
        """
        remove region by regionId
        :param args:
        :param kwargs:
        :return:
        """
        try:
            region_id = kwargs.get("regionId", 0)
            if not region_id:
                raise NotFound("Không có dữ liệu regionId")
            result = regions_model.delete(region_id)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("delete_region_by_id fail", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500
