# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import datetime
import json
from collections import OrderedDict

from playhouse.shortcuts import model_to_dict

from models.task import (MonthTask, WeekTask, TemporaryTask,
                         CommonTask, CommonTaskFrequency, TaskRecord, Category)


class DefaultListOrderedDict(OrderedDict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def get_commtasks_query(user_id, date):
    commtasks_query = CommonTask.select().where(
        (CommonTask.user_id == user_id) &
        (CommonTask.started_date <= date) &
        (CommonTask.finished_date >= date) &
        (CommonTask.status != CommonTask.DELETED)
    )
    return commtasks_query


def get_temptasks_query(user_id, date):
    temptasks = TemporaryTask.select().where(
                TemporaryTask.user_id == user_id,
                TemporaryTask.date == date,
                TemporaryTask.status != TemporaryTask.DELETED
                )
    return temptasks


def get_monthtasks_query(user_id, year, month_num):
    monthtasks_query = MonthTask.select().where(
        MonthTask.user_id == user_id,
        MonthTask.year == year,
        MonthTask.month == month_num,
        MonthTask.status != MonthTask.DELETED)
    return monthtasks_query


def get_weektasks_query(user_id, year, month_num, week_num):
    weektasks_query = WeekTask.select().where(
        WeekTask.user_id == user_id,
        WeekTask.year == year,
        WeekTask.month == month_num,
        WeekTask.weeknumber == week_num,
        WeekTask.status != WeekTask.DELETED)
    return weektasks_query


def get_commtasks_json(user_id, date, year, month_num):
    commtasks_dict = {}
    commtasks_query = get_commtasks_query(user_id, date)

    for com in commtasks_query:
        commtasks_dict[com.id] = {
            'content': com.content,
            'scheduled_started_at': com.scheduled_started_at,
            'scheduled_finished_at': com.scheduled_finished_at
        }
    commtasks_json = json.dumps(commtasks_dict, ensure_ascii=False)

    return commtasks_json


def get_temptasks_json(user_id, date):
    temptasks_dict = {}
    temptasks_query = get_temptasks_query(user_id, date)
    for t in temptasks_query:
        temptasks_dict[t.id] = {'content': t.content}
    temptasks_json = json.dumps(temptasks_dict)

    return temptasks_json


def get_monthtasks_json(user_id, year, month_num):
    monthtasks_dict = {}
    monthtasks_query = get_monthtasks_query(user_id, year, month_num)
    for m in monthtasks_query:
        monthtasks_dict[m.id] = {'content': m.content}
    monthtasks_json = json.dumps(monthtasks_dict)

    return monthtasks_json


def get_weektasks_json(user_id, year, month_num, week_num):
    weektasks_dict = {}
    weektasks_query = get_weektasks_query(user_id, year, month_num, week_num)
    for w in weektasks_query:
        weektasks_dict[w.id] = {'content': w.content}
    weektasks_json = json.dumps(weektasks_dict)

    return weektasks_json


def get_commtasks(user_id, date, year, month_num, weekday_num, day_num):
    commtasks_list = []
    commtasks_query = get_commtasks_query(user_id, date)

    for ct in commtasks_query:
        if CommonTaskFrequency.EVERYDAY in ct.frequency:
            commtasks_list.append(ct)
        elif weekday_num == 1:
            if CommonTaskFrequency.MONDAY in ct.frequency:
                commtasks_list.append(ct)
        elif weekday_num == 2:
            if CommonTaskFrequency.TUESDAY in ct.frequency:
                commtasks_list.append(ct)
        elif weekday_num == 3:
            if CommonTaskFrequency.WEDNESDAY in ct.frequency:
                commtasks_list.append(ct)
        elif weekday_num == 4:
            if CommonTaskFrequency.THURSDAY in ct.frequency:
                commtasks_list.append(ct)
        elif weekday_num == 5:
            if CommonTaskFrequency.FRIDAY in ct.frequency:
                commtasks_list.append(ct)
        elif weekday_num == 6:
            if CommonTaskFrequency.SATURDAY in ct.frequency:
                commtasks_list.append(ct)
        elif weekday_num == 7:
            if CommonTaskFrequency.SUNDAY in ct.frequency:
                commtasks_list.append(ct)

    commtasks = DefaultListOrderedDict()
    for ct in commtasks_list:
        ct_dict = model_to_dict(ct)
        ct_dict['finish_status'] = ct.finish_status(datetime.datetime.strptime(
            str(year)+'-'+str(month_num)+'-'+str(day_num),
            '%Y-%m-%d'
        ).date())
        ct_dict['scheduled_started_at'] = ct.scheduled_started_at
        ct_dict['scheduled_finished_at'] = ct.scheduled_finished_at

        commtasks[ct.category_id].append(ct_dict)

    return commtasks


def get_monthtasks(user_id, year, month_num):
    monthtasks = DefaultListOrderedDict()
    monthtasks_query = get_monthtasks_query(user_id, year, month_num)
    for mt in monthtasks_query:
        # for mt in mts:
            monthtasks[mt.category_id].append(model_to_dict(mt))
    return monthtasks


def get_weektasks(user_id, year, month_num, week_num):
    weektasks_query = get_weektasks_query(user_id, year, month_num, week_num)
    weektasks = DefaultListOrderedDict()
    for wt in weektasks_query:
        # for wt in wts:
            weektasks[wt.category_id].append(model_to_dict(wt))
    return weektasks