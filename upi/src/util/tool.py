# -*- coding:utf-8 -*-
"""
@author: LQG
@mail: linqigu@163.com
@file: tool.py
@time: 2021/10/16 22:56
@desc: 
"""
import json
import random
import re
import time


def data_is_json(data):
    """
    是否json
    :param data:
    :return: bool
    """
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def is_url(url):
    """
    是否是合法URL
    :param url:
    :return: bool
    """
    if re.match('^https?:/{2}\w.+$', url):
        return True
    return False


def get_rand(n):
    """
    获取随机数
    :param n:
    :return: string
    """
    string = []
    for i in range(n):
        string.append(str(random.randint(0, 9)))
    return ''.join(string)


def get_timestamp():
    """
    获取时间戳
    :return: int
    """
    t = time.time()
    return int(round(t * 1000))


def check_float(string):
    """
    判断输入的金额是否为正整数和正小数
    :param string:
    :return: bool
    """
    # 支付时，输入的金额可能是小数，也可能是整数
    s = str(string)
    if s.count('.') == 1:  # 判断小数点个数
        sl = s.split('.')  # 按照小数点进行分割
        left = sl[0]  # 小数点前面的
        right = sl[1]  # 小数点后面的
        if left.startswith('-') and left.count('-') == 1 and right.isdigit():
            lleft = left.split('-')[1]  # 按照-分割，然后取负号后面的数字
            if lleft.isdigit():
                return False
        elif left.isdigit() and right.isdigit():
            # 判断是否为正小数
            return True
    elif s.isdigit():
        s = int(s)
        if s != 0:
            return True
    return False


def get_order_no(n=30):
    """
    订单号
    :param n:
    :return: string
    """
    m = n - 14
    if m < 15:
        raise '订单号过短'
    s = [time.strftime("%Y%m%d%H%M%S")]
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(m):
        s.append(chars[random.Random().randint(0, length)])
    return "".join(s)


def trans_dict_to_xml(data_dict):
    """
    定义字典转XML的函数
    :param data_dict:
    :return: xml
    """
    data_xml = []
    for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
        v = data_dict.get(k)  # 取出字典中key对应的value
        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = '<![CDATA[{}]]>'.format(v)
        data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(data_xml)).encode('utf-8')  # 返回XML，并转成utf-8，解决中文的问题


def trans_xml_to_dict(data_xml):
    """
    定义XML转字典的函数
    :param data_xml:
    :return: dict
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict


class UpiException(Exception):
    """
    定义一个异常
    """

    def __init__(self, msg):
        super().__init__(msg)
