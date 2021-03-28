from flask import jsonify
from datetime import datetime
from app.extensions import api
from flask_restplus_patched import Resource
from app.libs.schema import common_schema

ns = api.namespace("healthCheck")


@ns.route("/")
class HealthCheckList(Resource):
    @ns.parameters(common_schema.HealthCheckParams())
    def get(self, args, **kwargs):
        data = {
            'status': "OK",
            'date': datetime.now(),
            'version': "0.0.2-beta"
        }
        return jsonify(data)
