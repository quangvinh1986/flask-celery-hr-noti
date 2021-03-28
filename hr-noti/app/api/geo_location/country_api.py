from flask import jsonify, current_app
from werkzeug.exceptions import NotFound
from app.libs.schema import geo_location_schema
from flask_restplus_patched import Resource
from app.extensions import api
from app.libs.common.logger import TraceException
from app.database_connect import countries_model
from app.libs.common.custom_exception import CustomControllerException, ERROR_MESSAGE

ns = api.namespace("geoLocation")


@ns.route("/countries")
class CountryAPI(Resource):
    @ns.parameters(geo_location_schema.CountriesGetAllParams())
    def get(self, args):
        """
        get all country in database
        :param args:
        :return:
        """
        try:
            limit = args.get("limit", 0)

            region_id = args.get("regionId", 0)
            if region_id:
                countries = countries_model.get_by_region_id(region_id, limit)
                return self.build_result(countries)

            country_name = args.get("countryName", "")
            if country_name:
                countries = countries_model.get_like_country_name(country_name, limit)
                return self.build_result(countries)

            countries = countries_model.get_all_case(limit)
            return self.build_result(countries)
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return jsonify({
                "text": trace.get_message(),
                "status_code": 500
            })

    def build_result(self, countries):
        lst_country = [country.get_json_serializeable() for country in countries]
        if lst_country:
            return lst_country, 200
        else:
            return [], 404

    @ns.parameters(geo_location_schema.CountriesPostParams(), locations=('json',))
    def post(self, args, **kwargs):
        """
        Cretate new country
        :param args:
        :param kwargs:
        :return:
        """
        try:
            data = args.copy()
            data['COUNTRY_NAME'] = args.get('countryName', "")
            data['REGION_ID'] = args.get('regionId', "")
            data['COUNTRY_ID'] = args.get('countryId', "")
            result = countries_model.add(data)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("update or add", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return {"text": trace.get_message()}, 500


@ns.route("/country/<countryId>")
class CountriesAPI(Resource):
    @ns.parameters(geo_location_schema.BlankParams())
    def get(self, args, **kwargs):
        """
        get country by countryId
        :param args:
        :param kwargs:
        :return:
        """
        country_id = kwargs.get("countryId", "")
        if not country_id:
            raise NotFound("Haven't parameter")
        try:
            country = countries_model.get_by_id(country_id)
            if country:
                return country
            else:
                return {}, 404
        except Exception as ex:
            trace = TraceException("", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500

    @ns.parameters(geo_location_schema.CountriesPostParams(), locations=('json',))
    def put(self, args, **kwargs):
        """
        update value of single country by countryId
        :param args:
        :param kwargs:
        :return:
        """
        country_id = kwargs.get("countryId", "")
        if not country_id:
            raise NotFound("Haven't parameter")
        try:
            data = dict()
            if args.get('countryName', False):
                data['COUNTRY_NAME'] = args.get('countryName', "")
            if args.get('regionId', False):
                data['REGION_ID'] = args.get('regionId', "")
            if args.get('countryId', False):
                data['COUNTRY_ID'] = args.get('countryId', "")
            result = countries_model.update(country_id, data)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("update ", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500

    @ns.parameters(geo_location_schema.BlankParams())
    def delete(self, args, **kwargs):
        """
        remove country by countryId
        :param args:
        :param kwargs:
        :return:
        """
        country_id = kwargs.get("countryId", "")
        if not country_id:
            raise NotFound("Haven't parameter")

        try:
            result = countries_model.delete(country_id)
            return result, 200
        except CustomControllerException:
            return ERROR_MESSAGE, 500
        except Exception as ex:
            trace = TraceException("delete_country_by_id fail", ex.__str__())
            current_app.logger.warning(trace.get_message())
            return ERROR_MESSAGE, 500
