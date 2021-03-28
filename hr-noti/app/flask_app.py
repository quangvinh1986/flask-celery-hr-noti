# -*- coding: utf-8 -*-
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_log_request_id import RequestID
from werkzeug.exceptions import default_exceptions
from app.sys_libs.exceptions import api_error_handler
from . import api
from .web_route import configure_route

# Config
from . import DEFAULT_CONFIG_CLASS, DEFAULT_APPLICATION_CONFIG_FILE, \
    DEFAULT_GLOBAL_CONFIG_FILE, load_module


def create_app(config=None):
    """Creates the app."""
    # Initialize the app
    app = Flask(__name__, static_url_path="", template_folder="")
    app.config.from_object(config)
    return app


def configure_app(app, filename=DEFAULT_GLOBAL_CONFIG_FILE,
                  config_class=DEFAULT_CONFIG_CLASS):
    """
    Configure a Flask app
    :param app:
    :param filename:
    :param config_class:
    :return:
    """
    # Select config file
    if not os.path.isfile(filename):
        filename = DEFAULT_APPLICATION_CONFIG_FILE

    # Load proper config for app
    config = load_module(filename)
    app.config.from_object(getattr(config, config_class))
    app.config.from_pyfile('./config_local.py', silent=True)

    # Correct LOG_FOLDER config
    app.config['LOG_FOLDER'] = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'logs')
    config.make_dir(app.config['LOG_FOLDER'])

    # Config Flask components
    RequestID(app)
    configure_route(app)
    configure_extensions(app)
    configure_blueprints(app)
    configure_log_handlers(app)
    configure_error_handlers(app)
    configure_after_request(app)


def configure_extensions(app):
    """
    Cấu hình các libs để sử dụng trong các ứng dụng khác.
    Thông thường dùng để truyền các config vào.

    :param app: flask app (main vsm_api)
    :return:
    """
    from .extensions import db, redis_db
    db.init_app(app)
    redis_db.init_app(app)

    # TODO: remove in PRODUCTION
    from .extensions import cors
    cors.init_app(app, resources={r"/my-api/*": {"origins": "*"}, r"/geo-location-/*": {"origins": "*"}})


def configure_blueprints(app):
    """
    Hàm khai báo các URL prefix cho phép sử dụng trong api
    :param app: Đối tượng flask app.
    :return:
    """
    api.init_app(app)


def configure_log_handlers(app):
    """
    Cấu hình logging của hệ
    :param app: flask app
    :return: not return
    """
    fmt = '%(asctime)s %(levelname)s: [in %(pathname)s:%(lineno)d] %(message)s'
    formatter = logging.Formatter(fmt)
    error_log = os.path.join(app.config['LOG_FOLDER'], app.config['APP_LOG'])
    error_file_handler = logging.handlers.RotatingFileHandler(error_log,
                                                              maxBytes=100000,
                                                              backupCount=10)
    error_file_handler.setLevel(logging.INFO)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    handler_console = logging.StreamHandler(stream=sys.stdout)
    handler_console.setFormatter(formatter)
    handler_console.setLevel(logging.INFO)
    app.logger.addHandler(handler_console)

    # set proper log level
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # unify log format for all handers
    for h in app.logger.handlers:
        h.setFormatter(formatter)

    app.logger.info('Config filename: {0}'.format(app.config['FILENAME']))
    app.logger.info('App log folder: {0}'.format(app.config['LOG_FOLDER']))


def configure_error_handlers(app):
    """Configures the error handlers."""

    for exception in default_exceptions:
        app.register_error_handler(exception, api_error_handler)
    app.register_error_handler(Exception, api_error_handler)


def init_indexs(mongo):
    """
    Create index for VSM
    ex:
        mongo.db.collection_name.create_index('key')
        mongo.db.collection_name.create_index([('key', ASCENDING)])
        mongo.db.collection_name.create_index([(‘key1′, ASCENDING), (‘key2′, DESCENDING)])
    """
    created_index = mongo.db.config.find_one(
        {"created_index": {"$in": [True, False]}}, {'id': 0})

    if not created_index or not created_index.get('created_index', False):
        # mongo.db.nvd.create_index('cve_id')
        mongo.db.config.update({"created_index": {"$in": [True, False]}},
                               {'$set': {'created_index': True}}, True)


def configure_after_request(app):
    @app.after_request
    def after_request(response):
        return response

#
# def configure_route(app):
#     @app.route('/download/<filename>')
#     # @valid_required
#     def download(filename):
#         # print("DownloadFile", filename)
#         return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
#
#     @app.route('/my-api/hello', methods=['GET', 'POST'])
#     def hook():
#         if request.method == 'GET':
#             return "Hello world!"
#         else:
#             return jsonify(message="unknow")
