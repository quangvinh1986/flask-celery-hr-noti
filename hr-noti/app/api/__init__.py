from flask import Blueprint
from .common import health_check
from .geo_location import region_api, location_api, country_api


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    api_v1_blueprint = Blueprint('api', __name__, url_prefix='/myApi')
    health_check.api.init_app(api_v1_blueprint)
    app.register_blueprint(api_v1_blueprint)
