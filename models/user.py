# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

from peewee import *
from .base import BaseModel


class User(BaseModel):
    username = CharField(max_length=25, default='')
    pwd = CharField(max_length=25, default='')
