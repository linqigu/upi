# -*- coding:utf-8 -*-
"""
@author: LQG
@mail: linqigu@163.com
@file: test_wx.py
@time: 2021/8/24 10:57
@desc: 
"""
import unittest

from upi import wxPay
from upi.util.tool import get_order_no


class test_wx_pay(unittest.TestCase):  # 继承unittest.TestCase

    def setUp(self):
        print('setUp')
        app_id = ''
        mch_id = ''
        mch_key = ''
        notify_url = ''

        self.pay = wxPay(
            app_id=app_id,
            mch_id=mch_id,
            mch_key=mch_key,
            notify_url=notify_url
        )

    def test_js_pay(self):
        print('test_js_pay')
        order_no = get_order_no()
        fee = 1
        open_id = 'oHQtp5NEePp-HaSVEgrvCjw9eKcw'  # 用户openid
        body = '支付详情说明'
        res = self.pay.js_pay(
            order_no=order_no,
            fee=fee,
            openid=open_id,
            body=body
        )
        print(res)

    def test_app_pay(self):
        print('test_app_pay')
        order_no = get_order_no()
        fee = 1
        body = '支付详情说明'

        res = self.pay.app_pay(
            order_no=order_no,
            fee=fee,
            body=body
        )
        print(res)

    def test_native_pay(self):
        print('test_native_pay')
        order_no = get_order_no()
        fee = 1
        body = '支付详情说明'
        res = self.pay.native_pay(
            order_no=order_no,
            fee=fee,
            body=body
        )
        print(res)

    def test_h5_pay(self):
        print('test_h5_pay')
        order_no = get_order_no()
        fee = 1
        body = '支付详情说明'
        res = self.pay.h5_pay(
            order_no=order_no,
            fee=fee,
            body=body
        )
        print(res)

    def test_mini_pay(self):
        print('test_mini_pay')
        order_no = get_order_no()
        fee = 1
        open_id = 'oHQtp5NEePp-HaSVEgrvCjw9eKcw'  # 用户openid
        body = '支付详情说明'
        res = self.pay.mini_pay(
            order_no=order_no,
            fee=fee,
            body=body,
            openid=open_id
        )
        print(res)
