# -*- coding:utf-8 -*-
"""
@author: LQG
@mail: linqigu@163.com
@file: log.py
@time: 2021/11/10 22:01
@desc: 日志模块
"""
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger()


def set_logger():
    LOG_FILENAME = 'log.log'
    logger.setLevel(logging.INFO)
    formatter = '%(asctime)s %(pathname)s[line:%(lineno)d] -%(process)d-%(threadName)s -%(levelname)s: %(message)s'
    vde_logging = logging.Formatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(vde_logging)
    logger.addHandler(console_handler)
    """
     info_handler = TimedRotatingFileHandler(
        filename=LOG_FILENAME,
        when='D',
        interval=1,
        backupCount=15,
        encoding='utf-8'
    )
    info_handler.setFormatter(vde_logging)
    logger.addHandler(info_handler)
    """

# set_logger()
