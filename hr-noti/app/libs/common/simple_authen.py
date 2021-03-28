from flask import current_app
import hashlib
import json
import jwt
# from app.lib.bpmapi.bpm_api import PMAPI
from app.libs.common.logger import TraceException


# def md5_hash(data):
#     md5hash = hashlib.md5()
#     md5hash.update(data.encode("utf8"))
#     return md5hash.hexdigest()
#
#
# def get_user_id(user_name):
#     try:
#         pm_api = PMAPI()
#         response = pm_api.get_user_info_by_user_name(user_name)
#         if response.status_code == 200:
#             list_data = json.loads(response.text, encoding='utf-8')
#             user_id = '00'
#             if len(list_data):
#                 for item in list_data:
#                     if item['usr_username'] == user_name:
#                         user_id = item['usr_uid']
#                         break
#             return user_id
#         else:
#             return '0000'
#     except Exception as ex:
#         trace = TraceException("get_user_id {}: {}".format(user_name, ex.__str__()))
#         current_app.logger.warning(trace.get_message())
#         return '000'
#
#
# def is_authenticated(headers):
#     """
#     Simplify authentication, will replace 'check_valid_token'
#     """
#     user_name = headers.get('UserName', '')
#     token = headers.get('MyToken', '')
#     user_id = get_user_id(user_name)
#     if user_id == '000' or user_id == '0000':
#         return False
#     for bmp_url in current_app.config.get('BPM_URLS').split(","):
#         my_token = md5_hash('{}{}'.format(user_id, bmp_url))
#         if my_token == token:
#             return True
#     else:
#         return False
#
#
# def jwt_valid_decode(user_name, token, module_name=''):
#     try:
#         payload = jwt.decode(token, current_app.config.get('KEY_SECRET'), algorithms=['HS256'])
#         user_id = get_user_id(user_name)
#         if user_id == '000' or user_id == '0000':
#             return False
#         if user_id == payload['userid']:
#             return True
#         else:
#             return False
#     except jwt.DecodeError:
#         return False
#     except Exception:
#         return False
