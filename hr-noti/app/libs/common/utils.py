"""
                    NOTICE TO DEV

Should includes only utilities specific to this API app.
Common function that can be shared with backoffice or ranking
should put to <strong>lib/common_utils.py</strong>

"""
# import jwt
from flask import jsonify, current_app, request
from marshmallow import fields, validate as validate_
from datetime import datetime, timedelta, date
from sqlalchemy import desc, asc


def format_desc(des):
    des = des.replace('\n', '<br/>')
    return des


def make_validator(val_str=None, val_int=None, val_dict=None):

    def custom_validator(obj):
        if isinstance(obj, str):
            if val_str:
                return val_str(obj)
            return True
        elif isinstance(obj, int):
            if val_int:
                return val_int(obj)
            return True
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if not custom_validator(k) or not custom_validator(v):
                    return False
        elif isinstance(obj, (list, tuple)):
            for v in obj:
                if not custom_validator(v):
                    return False
        return True

    return custom_validator


def get_version():
    return "ANI v0.1"


def send_result(data=None, message="OK", code=200, count=None):
    """
    :param data: simple result object like dict, string or list
    :type message:  Explaining the current status (e.g. what went wrong in an error result)
    :type code: HTTP status code or a numeric code corresponding to the error in an error result;
    :return: json rendered sting result
    """
    res = {
        "jsonrpc": "2.0",
        "status": True,
        "code": code,
        "message": message,
        "data": data,
        "version": get_version()
    }
    if count is not None:
        res.update({"count": count})
    return jsonify(res), 200


def send_error(data=None, message="Error", code=500):
    res_error = {
        "jsonrpc": "2.0",
        "status": False,
        "code": code,
        "message": message,
        "data": data,
        "version": get_version()
    }
    return jsonify(res_error), code


def pack_result(data=None, message="OK", code=200, count=None):
    """
    :param data: simple result object like dict, string or list
    :type message:  Explaining the current status (e.g. what went wrong in an error result)
    :type code: HTTP status code or a numeric code corresponding to the error in an error result;
    :return: json rendered sting result
    """
    res = {
        "jsonrpc": "2.0",
        "status": True,
        "code": code,
        "message": message,
        "data": data,
        "version": get_version()
    }
    if count is not None:
        res.update({"count": count})
    return res


def pack_error(data=None, message="Error", code=500):
    res_error = {
        "jsonrpc": "2.0",
        "status": False,
        "code": code,
        "message": message,
        "data": data,
        "version": get_version()
    }
    return res_error


def order_by(query, prop, dir):
    if dir == "desc":
        return query.order_by(desc(prop))
    else:
        return query.order_by(asc(prop))


def parse_req(argmap):
    return parser.parse(argmap)


def update_dict_by_obj(obj, target_obj, keys, prefix=''):
    for key in keys:
        if not hasattr(obj, key):
            continue

        target_obj.update({
            "{}{}".format(prefix, key): json_serial(getattr(obj, key))
        })

    return target_obj


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj


def build_query(args, table, query=None):
    if not query:
        query = {}

    for key, value in args:
        if key in table.c:
            query.update({
                table.c[key]: value
            })
    return query


class FieldString(fields.String):

    DEFAULT_MAX_LENGTH = 1024  # 1 kB

    def __init__(self, validate=None, **metadata):
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldString, self).__init__(validate=validate, **metadata)


class FieldTextFile(FieldString):
    DEFAULT_MAX_LENGTH = 1024*1024  # 1 MB