# -*- coding:utf-8 -*-
"""
@author: LQG
@mail: linqigu@163.com
@file: config.py
@time: 2021/11/10 22:59
@desc: 
"""
from enum import unique, Enum


@unique
class request_enum(Enum):
    # 超时时间
    API_TIME_OUT = 60
    # GET
    GET = 'GET'
    # POST
    POST = 'POST'
