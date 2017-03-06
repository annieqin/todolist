# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import datetime

from peewee import *
from .base import BaseModel

from lib.utils import time_to_string


class Category(BaseModel):
    DELETED = 0
    ENABLED = 1

    STATUS_CHOICES = (
        (DELETED, '已删除'),
        (ENABLED, '已启用')
    )

    MONTH = 1
    WEEK = 2
    DAY = 3

    LEVEL_CHOICES = (
        (MONTH, '月'),
        (WEEK, '周'),
        (DAY, '日')
    )
    user_id = IntegerField()
    content = CharField(max_length=25, default='')
    color = CharField(max_length=10, default='')
    level = IntegerField(choices=LEVEL_CHOICES, default=MONTH)
    status = IntegerField(choices=STATUS_CHOICES, default=ENABLED)


class CommonTask(BaseModel):
    PRIVATE = 1
    PUBLIC = 2

    VISIBLE_RANGE_CHOICES = (
        (PRIVATE, '仅自己可见'),
        (PUBLIC, '好友可见'),
    )

    DELETED = 0
    UNDELETED = 1

    STATUS = (
        (DELETED, '已删除'),
        (UNDELETED, '未删除')
    )

    user_id = IntegerField()

    category_id = IntegerField()

    status = IntegerField(choices=STATUS, default=UNDELETED)

    content = CharField(max_length=36, default='')
    visible_range = IntegerField(choices=VISIBLE_RANGE_CHOICES, default=PRIVATE)

    started_date = DateField(formats=['%Y-%m-%d'])
    finished_date = DateField(formats=['%Y-%m-%d'])

    @property
    def category(self):
        return Category.get(Category.id == self.category_id)

    def finish_status(self, date):
        status = TaskRecord.UNFINISHED
        try:
            status = TaskRecord.get(
                TaskRecord.commontask_id == self.id,
                TaskRecord.date == date
            ).status
        except TaskRecord.DoesNotExist:
            pass
        return status

    @property
    def frequency(self):
        frequencies = CommonTaskFrequency.select().where(
            CommonTaskFrequency.commontask_id == self.id
        )
        frequency = [f.frequency for f in frequencies]

        return frequency

    @property
    def scheduled_started_at(self):
        data = TaskRecord.get(
            TaskRecord.commontask_id == self.id
        ).scheduled_started_at

        return time_to_string(data.second) if data or data == datetime.timedelta(0) else ''

    @property
    def scheduled_finished_at(self):
        data = TaskRecord.get(
            TaskRecord.commontask_id == self.id
        ).scheduled_finished_at

        return time_to_string(data.second) if data or data == datetime.timedelta(0) else ''


class TemporaryTask(BaseModel):
    PRIVATE = 1
    PUBLIC = 2

    VISIBLE_RANGE_CHOICES = (
        (PRIVATE, '仅自己可见'),
        (PUBLIC, '好友可见'),
    )

    UNFINISHED = 0
    FINISHED = 1
    DELETED = 2

    STATUS = (
        (UNFINISHED, '未完成'),
        (FINISHED, '已完成'),
        (DELETED, '已删除')
    )
    user_id = IntegerField()

    content = CharField(max_length=36, default='')
    visible_range = IntegerField(choices=VISIBLE_RANGE_CHOICES, default=PRIVATE)
    date = DateField()
    scheduled_started_at = CharField(max_length=10, null=True)
    scheduled_finished_at = CharField(max_length=10, null=True)
    actual_started_at = CharField(max_length=10, null=True)
    actual_finished_at = CharField(max_length=10, null=True)
    status = IntegerField(choices=STATUS, default=UNFINISHED)
    comment = TextField(null=True)


class MonthTask(BaseModel):
    PRIVATE = 1
    PUBLIC = 2

    VISIBLE_RANGE_CHOICES = (
        (PRIVATE, '仅自己可见'),
        (PUBLIC, '好友可见'),
    )

    UNFINISHED = 0
    FINISHED = 1
    DELETED = 2

    STATUS = (
        (UNFINISHED, '未完成'),
        (FINISHED, '已完成'),
        (DELETED, '已删除')
    )
    user_id = IntegerField()

    year = IntegerField()
    month = IntegerField()

    content = CharField(max_length=36, default='')
    visible_range = IntegerField(choices=VISIBLE_RANGE_CHOICES, default=PRIVATE)
    status = IntegerField(choices=STATUS, default=UNFINISHED)
    comment = TextField(null=True)
    category_id = IntegerField()

    @property
    def category(self):
        return Category.get(Category.id == self.category_id)


class WeekTask(BaseModel):
    PRIVATE = 1
    PUBLIC = 2

    VISIBLE_RANGE_CHOICES = (
        (PRIVATE, '仅自己可见'),
        (PUBLIC, '好友可见'),
    )

    UNFINISHED = 0
    FINISHED = 1
    DELETED = 2

    STATUS = (
        (UNFINISHED, '未完成'),
        (FINISHED, '已完成'),
        (DELETED, '已删除')
    )
    user_id = IntegerField()

    year = IntegerField()
    month = IntegerField()
    weeknumber = IntegerField()

    content = CharField(max_length=36, default='')
    visible_range = IntegerField(choices=VISIBLE_RANGE_CHOICES, default=PRIVATE)
    status = IntegerField(choices=STATUS, default=UNFINISHED)
    comment = TextField(null=True)
    category_id = IntegerField()

    @property
    def category(self):
        return Category.get(Category.id == self.category_id)


class TaskRecord(BaseModel):
    UNFINISHED = 0
    FINISHED = 1

    STATUS = (
        (UNFINISHED, '未完成'),
        (FINISHED, '已完成'),
    )
    user_id = IntegerField()

    date = DateField(formats=['%Y-%m-%d'])
    weekday = CharField(max_length=20, default='')
    commontask_id = IntegerField(default=0)

    scheduled_started_at = TimeField(null=True, formats=['%H:%M'])
    scheduled_finished_at = TimeField(null=True, formats=['%H:%M'])
    actual_started_at = TimeField(null=True, formats=['%H:%M'])
    actual_finished_at = TimeField(null=True, formats=['%H:%M'])
    status = IntegerField(choices=STATUS, default=UNFINISHED)
    comment = TextField(null=True)


class CommonTaskFrequency(BaseModel):
    EVERYDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    FREQUENCY = (
        (EVERYDAY, '每天'),
        (MONDAY, '每周一'),
        (TUESDAY, '每周二'),
        (WEDNESDAY, '每周三'),
        (THURSDAY, '每周四'),
        (FRIDAY, '每周五'),
        (SATURDAY, '每周六'),
        (SUNDAY, '每周日')
    )
    commontask_id = IntegerField(default=0)
    frequency = IntegerField(choices=FREQUENCY, default=EVERYDAY)



