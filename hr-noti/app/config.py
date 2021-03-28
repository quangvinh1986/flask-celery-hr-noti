# -*- coding: utf-8 -*-
import os
from pathlib import Path


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e


class DefaultConfig(object):
    DEBUG = False
    FILENAME = __file__

    # <editor-fold desc="Constan">
    USERNAME_EXP = "^[a-zA-Z][a-zA-Z0-9_]{4,29}$"
    PWD_EXP = "^((?=(.*[a-zA-Z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s)).{8,}$"
    PHONE_EXP = "^\+?[0-9 ]*$"
    IP_DOMAIN_EXP = "^(([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,10})|((?:(?:25[0-5]|2[0-4][0-9]" \
                    "|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))$"

    COOKIE_MAX_AGE = 2147483647
    SESSION_TIME_DELTA = 60
    COOKIE_SECURE = False
    # COOKIE_DOMAIN = "127.0.0.1"

    # </editor-fold>

    # Security
    # This is the secret key that is used for session signing.
    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = "Fixed for test"
    # The filename for the info and error logs. The logfiles are stored at log-api/logs
    APP_LOG = "app.log"
    ERROR_LOG = "error.log"
    current_path = os.path.dirname(__file__)
    LOG_FOLDER = os.path.join(os.path.abspath(os.path.dirname(current_path)),
                              'logs')


class ApiAppConfig(DefaultConfig):
    """Special config for API"""

    # <editor-fold desc="Must be change by DevOps">

    path_file = os.path.abspath(os.path.dirname(__file__))
    main_folder = Path(os.path.abspath(os.path.dirname(__file__))).parent

    # [SSL Cert]
    PEM_TYPE = "LOCAL"
    if PEM_TYPE == 'LOCAL':
        main_folder = Path(os.path.abspath(os.path.dirname(__file__))).parent
        CERT_PEM = os.path.join(main_folder, "cert.pem")
        KEY_PEM = os.path.join(main_folder, "key.pem")
    else:
        CERT_PEM = "cert.pem"
        KEY_PEM = "key.pem"

    # LOG
    LOG_FOLDER = "logs"
    LOG_PATH = os.path.join(main_folder, "logs")

    _upload_folder = "Temp_Upload"
    UPLOAD_FOLDER = os.path.join(Path(os.path.abspath(os.path.dirname(__file__))).parent, _upload_folder)

    HEALTH_CHECK_URL = 'http://127.0.0.1:5001/myApi/healthCheck'

    # [REDIS]
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 1
    REDIS_PASSWORD = None
    # REDIS_PASSWORD = "redispassword"

    if REDIS_PASSWORD:
        REDIS_URL = 'redis://:{0}{1}:{2}/{3}'.format(REDIS_PASSWORD + "@", REDIS_HOST, REDIS_PORT, REDIS_DB)
    else:
        REDIS_URL = 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)

    result_backend = REDIS_URL
    broker_url = REDIS_URL

    RESULT_BACKEND = REDIS_URL
    BROKER_URL = REDIS_URL
    # </editor-fold>


class TestingConfig(ApiAppConfig):
    TESTING = True
    DEBUG = True
