from flask import current_app
from werkzeug.exceptions import NotFound
from app.libs.schema import geo_location_schema
from flask_restplus_patched import Resource
from app.extensions import api
from app.libs.common.logger import TraceException
from app.libs.common.custom_exception import ERROR_MESSAGE, CustomControllerException
from app.database_connect import location_model

ns = api.namespace("geoLocation")


@ns.route("/locations")
class LocationssAPI(Resource):
    @ns.parameters(geo_location_schema.LocationsGetAllParams())
    def get(self, args):
        """
        get all location in database
        :param args:
        :return:
        """
        try:
            limit = args.get("limit", 0)
            city_name = args.get("cityName", "")
            if city_name:
                locations = location_model.get_by_city(city_name, limit)
                return self.build_result(locations)
            country_id = args.get('countryId')
            if country_id:
                locations = location_model.get_all_case(city_name, limit)
                return self.build_result(locations)
            locations = location_model.get_all_case(city_name, limit)
            return self.build_result(locations)
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500

    def build_result(self, locations):
        lst_locations = [location.get_json_serializeable() for location in locations]
        if lst_locations:
            return lst_locations, 200
        else:
            return [], 404

    @ns.parameters(geo_location_schema.LocationsPostParams(), locations=('json',))
    def post(self, args):
        """
        create new location
        :param args:
        :return:
        """
        try:
            data = dict()
            data['STREET_ADDRESS'] = args.get('streetAddress', "")
            data['POSTAL_CODE'] = args.get('postalCode', "")
            data['CITY'] = args.get('city', "")
            data['STATE_PROVINCE'] = args.get('stateProvince', "")
            data['COUNTRY_ID'] = args.get('countryId', "")
            result = location_model.add(data)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("update or add", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500

    @ns.parameters(geo_location_schema.LocationDeleteParams(), locations=('json',))
    def delete(self, args):
        """
        delete multi record.
        :param args:
        :return:
        """
        try:
            list_id = args.get('listId', [])
            result = location_model.multi_delete(list_id)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("multi delete", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500


@ns.route("/locaton/<locationId>")
class LocationsAPI(Resource):
    @ns.parameters(geo_location_schema.BlankParams())
    def get(self, args, **kwargs):
        """
        get single location by locationId
        :param args:
        :param kwargs:
        :return:
        """
        try:
            location_id = kwargs.get("locationId", 0)
            if not location_id:
                raise NotFound("Không có dữ liệu locationId")
            location = location_model.get_by_id(location_id)
            return location, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("get_location_by_id fail", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500

    @ns.parameters(geo_location_schema.LocationsPostParams(), locations=('json',))
    def put(self, args, **kwargs):
        """
        Update location by locationId
        :param args:
        :param kwargs:
        :return:
        """
        try:
            data = dict()
            location_id = kwargs.get("locationId", 0)
            if not location_id:
                raise NotFound("Không có dữ liệu locationId")
            result = location_model.update(data, location_id)
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
        remove location by locationId
        :param args:
        :param kwargs:
        :return:
        """
        try:
            location_id = kwargs.get("locationId", 0)
            if not location_id:
                raise NotFound("Không có dữ liệu locationId")
            result = location_model.delete(location_id)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("delete_location_by_id fail", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500
