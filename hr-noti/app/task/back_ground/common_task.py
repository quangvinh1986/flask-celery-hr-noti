import json
import requests
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class CommonTask:

    def __init__(self, config):
        self.config = config

    def __get_request(self, request_url):
        header = {"Content-Type": "application/json"}
        resp = requests.get(request_url, headers=header, allow_redirects=False, verify=False)
        return resp

    def _get_request(self, request_url):
        req = requests.session()
        header = {"Content-Type": "application/json"}
        req.headers.update(header)
        req.verify = False
        resp = req.get(request_url)
        return resp

    def do_health_check(self):
        request_url = self.config.get('HEALTH_CHECK_URL', "")
        if request_url:
            resp = self._get_request(request_url)
            if resp.status_code == 200:
                logger.info("HealthCheck SUCCESS: {}".format(json.dumps(resp.text)))
                return True
            else:
                logger.error("HealthCheck FAIL: {}".format(json.dumps(resp.text)))
                return False
        else:
            logger.error("Can't find request url in configuration")
            return False
