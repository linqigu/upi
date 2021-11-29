# -*- coding:utf-8 -*-
"""
@author: LQG
@mail: linqigu@163.com
@file: wxpay.py
@time: 2021/10/16 22:54
@desc: 
"""
import hashlib

import requests
from enum import Enum, unique

from upi.config import request_enum
from upi.util.tool import is_url, get_timestamp, check_float, trans_dict_to_xml, trans_xml_to_dict, UpiException
from upi.util.log import logger, set_logger


@unique
class wx_pay_enum(Enum):
    # 主
    PAY_HOST_MASTER = "https://api.mch.weixin.qq.com"
    # 统一下单接口
    PAY_URL_UNIFIED_ORDER = '/pay/unifiedorder'
    # 普通商户
    MERCHANT_GENERAL = "GENERAL"
    # 服务商
    MERCHANT_SERVICE = "SERVICE"
    # 银行商户
    MERCHANT_BANK = "BANK"
    # 公众号支付
    JS_PAY = 101
    # APP 支付
    APP_PAY = 102
    # H5支付
    H5_PAY = 103
    # 扫码支付
    NATIVE_PAY = 104
    # 小程序支付
    MINI_PAY = 105
    # TRADE_TYPE 类型JSAPI
    TRADE_TYPE_JS = 'JSAPI'
    # TRADE_TYPE 类型APP
    TRADE_TYPE_APP = 'APP'
    # TRADE_TYPE 类型H5
    TRADE_TYPE_H5 = 'MWEB'
    # TRADE_TYPE 扫码支付
    TRADE_TYPE_NATIVE = 'NATIVE'


class wxPay(object):
    def __init__(self,
                 app_id,
                 mch_id,
                 mch_key,
                 notify_url,
                 sub_app_id=None,
                 sub_mch_id=None,
                 mch_type=wx_pay_enum.MERCHANT_GENERAL.value,
                 api_time_out=request_enum.API_TIME_OUT.value,
                 pay_host=wx_pay_enum.PAY_HOST_MASTER.value,
                 logger_echo=False
                 ):
        """

        :param app_id: app_id 支付appid
        :param mch_id: 商户号
        :param mch_key: 商户密钥
        :param notify_url: 回调通知地址
        :param sub_app_id: 子商户app_id
        :param sub_mch_id: 子商户号
        :param mch_type: 商户类型，默认普通商户
        :param api_time_out: 接口超时时间 默认60S
        :param pay_host:  调用接口地址 默认 https://api.mch.weixin.qq.com
        :param logger_echo: 是否输出日志 True False  默认False
        """
        self.app_id = app_id
        self.mch_id = mch_id
        self.sub_app_id = sub_app_id
        self.sub_mch_id = sub_mch_id
        self.mch_key = mch_key
        self.notify_url = notify_url
        self.mch_type = mch_type
        self.api_time_out = api_time_out
        self.pay_host = pay_host
        if logger_echo:
            set_logger()
        self.__check_common()
        logger.info('微信支付实例化完成')

    def js_pay(self, order_no, fee, body, openid, goods_tag=None, attach=None):
        """
        JS支付
        :param order_no:  订单号
        :param fee:  支付金额 单位分
        :param body: 支付详情 例：XXX商品
        :param openid: 微信用户openid
        :param goods_tag: 优惠券标识
        :param attach: 回调原样返回
        :return:
        """
        return self.__package_pay_data(order_no, fee, body, goods_tag, attach, apply_type=wx_pay_enum.JS_PAY.value,
                                       openid=openid)

    def app_pay(self, order_no, fee, body, goods_tag=None, attach=None):
        """
        APP支付
        :param order_no:  订单号
        :param fee:  支付金额 单位分
        :param body: 支付详情 例：XXX商品
        :param goods_tag: 优惠券标识
        :param attach: 回调原样返回
        :return:
        """
        return self.__package_pay_data(order_no, fee, body, goods_tag, attach, apply_type=wx_pay_enum.APP_PAY.value)

    def native_pay(self, order_no, fee, body, goods_tag=None, attach=None):
        """
        二维码支付
        :param order_no:  订单号
        :param fee:  支付金额 单位分
        :param body: 支付详情 例：XXX商品
        :param goods_tag: 优惠券标识
        :param attach: 回调原样返回
        :return:
        """
        return self.__package_pay_data(order_no, fee, body, goods_tag, attach, apply_type=wx_pay_enum.NATIVE_PAY.value)

    def h5_pay(self, order_no, fee, body, goods_tag=None, attach=None):
        """
        H5支付
       :param order_no:  订单号
       :param fee:  支付金额 单位分
       :param body: 支付详情 例：XXX商品
       :param goods_tag: 优惠券标识
       :param attach: 回调原样返回
       :return:
       """
        return self.__package_pay_data(order_no, fee, body, goods_tag, attach, apply_type=wx_pay_enum.H5_PAY.value)

    def mini_pay(self, order_no, fee, body, openid, goods_tag=None, attach=None):
        """
        小程序支付
        :param order_no:  订单号
        :param fee:  支付金额 单位分
        :param body: 支付详情 例：XXX商品
        :param openid: 微信用户openid
        :param goods_tag: 优惠券标识
        :param attach: 回调原样返回
        :return:
        """
        return self.__package_pay_data(order_no, fee, body, goods_tag, attach, apply_type=wx_pay_enum.JS_PAY.value,
                                       openid=openid)

    def __package_pay_data(self, order_no, fee, body, goods_tag, attach, apply_type, openid=None):
        """
        封装请示数据
        :param order_no:订单号
        :param fee:支付金额 单位分
        :param body:支付详情 例：XXX商品
        :param goods_tag:优惠券标识
        :param attach:回调原样返回
        :param apply_type: 支付类型
        :param openid:微信用户openid
        :return:
        """
        if len(order_no) > 32 or len(order_no) < 12:
            raise UpiException("订单号不合法")
        if not check_float(fee):
            raise UpiException("输入金额有误")
        pay_detail = {
            "appid": self.app_id,
            "mch_id": self.mch_id,
            "nonce_str": order_no,
            "body": body,
            "out_trade_no": order_no,
            "total_fee": fee,
            "spbill_create_ip": "127.0.0.1",
            "notify_url": self.notify_url
        }

        if goods_tag is not None:
            pay_detail["goods_tag"] = goods_tag
        if attach is not None:
            pay_detail["attach"] = attach
        if self.mch_type == wx_pay_enum.MERCHANT_GENERAL.value:
            # 为普通商户
            pass
        elif self.mch_type == wx_pay_enum.MERCHANT_SERVICE.value:
            # 服务商
            pay_detail["sub_app_id"] = self.sub_app_id
            pay_detail["sub_mch_id"] = self.sub_mch_id
        elif self.mch_type == wx_pay_enum.MERCHANT_BANK.value:
            # 银行商户
            raise UpiException("当前sdk不支付银行商户支付")
        res = {'pay_data': None}
        self.request_url = "".join([self.pay_host, wx_pay_enum.PAY_URL_UNIFIED_ORDER.value])
        if apply_type in [wx_pay_enum.JS_PAY.value, wx_pay_enum.MINI_PAY.value]:
            # 公众号支持与小程序支付一致
            pay_detail['trade_type'] = wx_pay_enum.TRADE_TYPE_JS.value
            pay_detail['openid'] = openid
            pay_detail["sign"] = self.__sign(pay_detail)
            r = self.__js_package(self.__send_request(pay_detail))
            res.update({'pay_data': r})
        if apply_type == wx_pay_enum.NATIVE_PAY.value:
            pay_detail['trade_type'] = wx_pay_enum.TRADE_TYPE_NATIVE.value
            pay_detail["sign"] = self.__sign(pay_detail)
            r = self.__send_request(pay_detail)
            res.update({'pay_data': r['code_url']})
        if apply_type == wx_pay_enum.H5_PAY.value:
            pay_detail['trade_type'] = wx_pay_enum.TRADE_TYPE_H5.value
            pay_detail["sign"] = self.__sign(pay_detail)
            r = self.__send_request(pay_detail)
            res.update({'pay_data': r['mweb_url']})
        if apply_type == wx_pay_enum.APP_PAY.value:
            pay_detail['trade_type'] = wx_pay_enum.TRADE_TYPE_APP.value
            pay_detail["sign"] = self.__sign(pay_detail)
            r = self.__js_package(self.__send_request(pay_detail))
            res.update({'pay_data': r})
        return res

    def __js_package(self, result):
        """
        计算JS与小程序签名再返回
        :param result:
        :return:
        """
        payTime = get_timestamp()
        pay_data = {
            "appId": result["appid"],
            "nonceStr": result["nonce_str"],
            "package": "prepay_id=" + result["prepay_id"],
            "signType": "MD5",
            "timeStamp": payTime
        }
        pay_data["paySign"] = self.__sign(pay_data)
        return pay_data

    def __send_request(self, detail):
        """
        发送微信支付请求
        :param detail:
        :return:
        """
        logger.info('请求报文:{}'.format(detail))
        logger.info('请求URL:{}'.format(self.request_url))

        xml = trans_dict_to_xml(detail)
        start_time = get_timestamp()
        # 以POST方式向微信公众平台服务器发起请求
        try:
            response = requests.request(request_enum.POST.value, self.request_url, data=xml, timeout=self.api_time_out)
        except Exception as e:
            raise UpiException(e)

        logger.info('请求响应时间:{}{}'.format(str(get_timestamp() - start_time), 'ms'))
        result = response.content
        result = trans_xml_to_dict(result)
        logger.info('响应报文:{}'.format(result))
        if result['return_code'] != 'SUCCESS':
            raise UpiException(result["return_msg"])
        if result['result_code'] != 'SUCCESS':
            raise UpiException(result["err_code_des"])
        return result

    def __sign(self, data_dict):
        """
        # # 签名函数，参数为签名的数据和密钥
        # params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
        # params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
        # # 组织参数字符串并在末尾添加商户交易密钥
        # md5 = hashlib.md5()  # 使用MD5加密模式
        # md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
        # sign = md5.hexdigest().upper()  # 完成加密并转为大写
        # return sign
        :param data_dict:
        :return:
        """
        stringA = ''
        key = self.mch_key
        ks = sorted(data_dict.keys())
        # 参数排序
        for k in ks:
            if k != "sign":
                v = str(data_dict[k])
                stringA += (k + '=' + v + '&')
        # 拼接商户KEY
        stringSignTemp = stringA + "key=" + key
        # md5加密,也可以用其他方式
        hash_md5 = hashlib.md5(stringSignTemp.encode('utf8'))
        sign = hash_md5.hexdigest().upper()
        return sign

    def __check_common(self):
        """
        支付公共参数判断
        :return:
        """
        logger.info('开始检测公共参数')
        if self.mch_type not in [wx_pay_enum.MERCHANT_GENERAL.value, wx_pay_enum.MERCHANT_SERVICE.value,
                                 wx_pay_enum.MERCHANT_BANK.value]:
            raise UpiException("商户号类型输入错误,您输入的为:{}".format(self.mch_type))
        if self.mch_type == wx_pay_enum.MERCHANT_SERVICE.value:
            if self.sub_app_id is None:
                raise UpiException("服务商商户sub_app_id必传")
            if self.sub_mch_id is None:
                raise UpiException("服务商商户sub_mch_id必传")
        if self.mch_type == wx_pay_enum.MERCHANT_BANK.value:
            raise UpiException("当前sdk不支付银行商户支付")
        # 检测回调地址是否合法
        if not is_url(self.notify_url):
            raise UpiException("notify_url不合法")
        logger.info('检测公共参数完毕')
