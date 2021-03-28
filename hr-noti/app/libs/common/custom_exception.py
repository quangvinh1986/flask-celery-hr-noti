import logging

logger = logging.getLogger(__name__)

ERROR_MESSAGE = {'error': 'Something when wrong, please contact administrator', 'status': "NOK"}
OK_MESSAGE = {'status': 'OK'}

class CustomControllerException(Exception):
    def __init__(self, message):
        self.message = message
        logger.warning(message)

    def __str__(self):
        return self.message
