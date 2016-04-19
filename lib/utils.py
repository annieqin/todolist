# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import calendar
import json
from datetime import datetime, timedelta

from playhouse.shortcuts import model_to_dict, dict_to_model

from .datetimejson import LazableJSONEncoder


def num_to_string(num, type):
    if type == 'month':
        months = ['January', 'February', 'March', 'April',
                  'May', 'June', 'July', 'August', 'September',
                  'October', 'November', 'December']
        ret = months[num - 1]
        return ret
    elif type == 'weekday':
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ret = weekdays[num - 1]
        return ret
    elif type == 'week' or 'day':
        if num == 1:
            ret = '1st'
        elif num == 2:
            ret = '2nd'
        elif num == 3:
            ret = '3rd'
        else:
            ret = str(num)+'th'
        return ret


def parse_json(data):
    return json.loads(data.request.body)


# def obj_to_json(obj):
#     return json.dumps(model_to_dict(obj), cls=LazableJSONEncoder)
#
#
# def json_to_obj(model, json):
#     return dict_to_model(model, json.loads(json))

def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def int_to_time(data):
    hour = int(data) / 60
    minute = int(data) % 60
    ret = ''
    if minute < 10:
        minute = str(0)+str(minute)
    if hour == 0:
        ret = str(hour+12)+':'+str(minute)+'am'
    elif 0 < hour < 12:
        ret = str(hour)+':'+str(minute)+'am'
    elif 12 <= hour < 24:
        ret = str(hour)+':'+str(minute)+'pm'
    return ret


def time_to_string(data):
    hour = data / 3600
    minute = (data % 3600) / 60
    ret = ''
    if minute < 10:
        minute = str(0)+str(minute)
    if hour == 0:
        ret = str(hour+12)+':'+str(minute)+'am'
    elif 0 < hour < 12:
        ret = str(hour)+':'+str(minute)+'am'
    elif hour == 12:
        ret = str(hour)+':'+str(minute)+'pm'
    elif 12 < hour < 24:
        ret = str(hour-12)+':'+str(minute)+'pm'
    return ret








