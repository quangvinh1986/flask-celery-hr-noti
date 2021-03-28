#
#  Shared api schema between frontend and backend
#
#  Naming Rule:
#  <Api package name><Function name><Parameter>
#  Ex: AdminListParameter, AdminEditParameter,
#

from flask_marshmallow import base_fields
from marshmallow import validate
from flask_restplus_patched import Parameters
from .common_schema import BlankParams


# <editor-fold desc="Region Params">
class RegionsGetAllParams(Parameters):
    limit = base_fields.Integer()
    regionName = base_fields.String()


class RegionsDeleteParams(Parameters):
    listId = base_fields.List(base_fields.Integer())


class RegionsPostParams(Parameters):
    regionName = base_fields.String()
# </editor-fold>


# <editor-fold desc="Country Params">
class CountriesGetAllParams(Parameters):
    limit = base_fields.Integer()
    regionId = base_fields.Integer()
    countryName = base_fields.String()


class CountriesDeleteParams(Parameters):
    listId = base_fields.List(base_fields.Integer())


class CountriesPostParams(Parameters):
    regionId = base_fields.Integer()
    countryName = base_fields.String()
    countryId = base_fields.String()


class CountryDeleteParams(Parameters):
    CountryId = base_fields.List(base_fields.String())
# </editor-fold>


# <editor-fold desc="Locations Params">
class LocationsGetAllParams(Parameters):
    limit = base_fields.Integer()
    countryId = base_fields.String()
    cityName = base_fields.String()


class LocationDeleteParams(Parameters):
    listId = base_fields.List(base_fields.Integer())


class LocationsPostParams(Parameters):
    streetAddress = base_fields.String()
    postalCode = base_fields.String()
    city = base_fields.String()
    stateProvince = base_fields.String()
    countryId = base_fields.String()
# </editor-fold>
