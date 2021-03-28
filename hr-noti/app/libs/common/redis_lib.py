from app.extensions import redis_db
from flask import json, current_app
from app.libs.common.logger import TraceException
from uuid import uuid4
from datetime import datetime, timedelta


def save_all_to_redis(result, key, time_expire=21600):
    try:
        my_hash = redis_db.Hash(key)
        my_hash[key] = json.dumps(result)
        if time_expire:
            redis_db.expire(key, time_expire)

    except Exception as ex:
        trace = TraceException("save_all_to_redis fail ", key, ex.__str__())
        current_app.logger.warning(trace)


def get_all_from_redis(key):
    try:
        my_hash = redis_db.Hash(key)
        if my_hash:
            my_dict = my_hash[key]
            if my_dict:
                return json.loads(my_dict)
            else:
                return {}
        else:
            return {}
    except Exception as ex:
        trace = TraceException("get_all_from_redis fail ", key, ex.__str__())
        current_app.logger.warning(trace)
        return {}


def update_list(data, list_key, time_expire=21600):
    """
    List structure => List of hash key
    Hash => store data (dictionary)
    """
    try:
        # data is value of hash should be update into list
        hash_key = uuid4()

        # set value to hash
        my_hash = redis_db.Hash(hash_key)
        my_hash.update(data)
        if time_expire:
            redis_db.expire(hash_key, time_expire)

        # set add hash key to list
        my_list = redis_db.List(list_key)
        my_list.extend([hash_key])
        if time_expire:
            redis_db.expire(list_key, time_expire)
    except Exception as ex:
        trace = TraceException("save list to redis fail ", list_key, ex.__str__())
        current_app.logger.warning(trace)


def get_list_data(key):
    try:
        results = []
        my_list = redis_db.List(key)

        if my_list:
            for hash_key in my_list:
                data = redis_db.Hash(hash_key)
                if data:
                    data = {str(key, "utf-8"): str(value, "utf-8") for key, value in data}
                    results.append(data)

        return results
    except Exception as ex:
        trace = TraceException("save_all_to_redis fail ", key, ex.__str__())
        current_app.logger.warning(trace)
        return []


def add_cache_transref(key, value, time_expire=172800):
    """

    :param key:
    :param value:
    :param time_expire: value in second, 172800 seconds are 2 days
    :return:
    """
    today = datetime.now()
    key_today = today.strftime("%Y%m%d")
    if not redis_db.Hash(key_today):
        my_hash = redis_db.Hash(key_today)
        my_hash[key] = value
        redis_db.expire(key_today, time_expire)
    else:
        my_hash = redis_db.Hash(key_today)
        my_hash[key] = value


def has_cache_transref(key):
    """

    :param key:
    :return: True/False
    """
    today = datetime.now()
    last_day = today - timedelta(days=1)
    key_today = today.strftime("%Y%m%d")
    key_last_day = last_day.strftime("%Y%m%d")

    if redis_db.Hash(key_today):
        hash_today = redis_db.Hash(key_today)
        if hash_today[key]:
            return True

    if redis_db.Hash(key_last_day):
        hash_last_day = redis_db.Hash(key_last_day)
        if hash_last_day[key]:
            return True

    return False


def get_cache_transref(key):
    """

    :param key:
    :return: Value of key or None
    """
    today = datetime.now()
    last_day = today - timedelta(days=1)
    key_today = today.strftime("%Y%m%d")
    key_last_day = last_day.strftime("%Y%m%d")

    if redis_db.Hash(key_today) and redis_db.Hash(key_today)[key]:
        return str(redis_db.Hash(key_today)[key])

    if redis_db.Hash(key_last_day) and redis_db.Hash(key_last_day)[key]:
        return str(redis_db.Hash(key_last_day)[key])

    return None


def remove_cache_transref(key):
    """

    :param key:
    :return: Value of key or None
    """
    try:
        today = datetime.now()
        last_day = today - timedelta(days=1)
        key_today = today.strftime("%Y%m%d")
        key_last_day = last_day.strftime("%Y%m%d")

        if redis_db.Hash(key_today) and redis_db.Hash(key_today)[key]:
            del redis_db.Hash(key_today)[key]
            return True
            # return str(redis_db.Hash(key_today)[key])

        if redis_db.Hash(key_last_day) and redis_db.Hash(key_last_day)[key]:
            del redis_db.Hash(key_last_day)[key]
            return True

        return False
    except Exception as ex:
        return  False




def clear_list_data(key):
    try:
        results = []
        my_list = redis_db.List(key)

        if my_list:
            for hash_key in my_list:
                data = redis_db.Hash(hash_key)
                data.clear()
        my_list.clear()

        return results
    except Exception as ex:
        trace = TraceException("delete_list_data_failed ", key, ex.__str__())
        current_app.logger.warning(trace)
        return []
