# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

from peewee import *
# from .task import (TemporaryTask, TaskRecord, CommonTask,
#                    Category, MonthTask, WeekTask)
# from .user import User

mysql_db = MySQLDatabase('todolist', host='127.0.0.1', port=3306, user='root')


# def create_tables():
#     mysql_db.connect()
#     mysql_db.create_tables([CommonTask,
#                             TemporaryTask,
#                             TaskRecord,
#                             User,
#                             Category,
#                             MonthTask,
#                             WeekTask], safe=True)


class BaseModel(Model):
    class Meta:
        database = mysql_db