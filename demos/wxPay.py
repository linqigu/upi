# -*- coding:utf-8 -*-
"""
@author: LQG
@mail: linqigu@163.com
@file: wxPay.py
@time: 2021/11/29 22:40
@desc: 
"""
from upi import wxPay
from upi.util.tool import get_order_no

app_id = ''
mch_id = ''
mch_key = ''
notify_url = ''


order_no = get_order_no()
fee = 1
open_id = 'oHQtp5NEePp-HaSVEgrvCjw9eKcw'  # 用户openid
body = '支付详情说明'


pay = wxPay(
    app_id=app_id,
    mch_id=mch_id,
    mch_key=mch_key,
    notify_url=notify_url,
    logger_echo=True
)

pay_data = pay.js_pay(
    order_no=order_no,
    fee=fee,
    openid=open_id,
    body=body
)
print(pay_data)