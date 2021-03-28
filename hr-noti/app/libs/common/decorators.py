from functools import wraps
from flask import request
from werkzeug.exceptions import Forbidden
from . import simple_authen


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # if not simple_authen.is_authenticated(request.headers):
        #     raise Forbidden('Forbidden-Truy nhap khong hop le with headers: {}'.format(request.headers))
        return f(*args, **kwargs)
    return decorated_function

