from flask import jsonify, request, current_app
from datetime import datetime
from app.extensions import api
from flask_restplus_patched import Resource
from app.libs.schema import common_schema
from app.task import celery

ns = api.namespace("task")


@ns.route('/registerTask/<taskName>/<countDown>')
class RegisterTaskByNameAPI(Resource):
    @ns.parameters(common_schema.BlankParams(), locations=('json',))
    def post(self, args, **kwargs):
        """
        send a request to register background task

        :param args:
        :param kwargs:
        :return:
        """
        data = request.json
        task_name = kwargs.get("taskName", "")
        count_down = kwargs.get("countDown", 0)
        data_string = "Receive data to register task {} from {} content {}".\
            format(task_name, request.remote_addr, str(data))
        current_app.logger.info(data_string)
        if data:
            celery.send_task(task_name, args=[data], countdown=int(count_down))
        else:
            celery.send_task(task_name, args=[], countdown=int(count_down))
        return "send task success!", 200
