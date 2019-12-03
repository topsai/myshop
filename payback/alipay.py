#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/11/24 23:48
@Author:  "范斯特罗夫斯基" John
@File: alipay.py
@Software: PyCharm
"""
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from base64 import decodebytes, encodebytes
import json

import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')


class AliPay(object):
    """
    支付宝支付接口(PC端支付接口)
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        # self.appid = appid
        # self.app_notify_url = app_notify_url
        # self.app_private_key = None
        # self.return_url = return_url
        # with open(self.app_private_key_path) as fp:
        #     self.app_private_key = RSA.importKey(fp.read())
        # self.alipay_public_key_path = alipay_public_key_path
        # with open(self.alipay_public_key_path) as fp:
        #     self.alipay_public_key = RSA.importKey(fp.read())
        #
        # if debug is True:
        #     self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        # else:
        #     self.__gateway = "https://openapi.alipay.com/gateway.do"

        """
            设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
            """
        alipay_client_config = AlipayClientConfig(sandbox_debug=True)
        alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
        alipay_client_config.app_id = appid
        with open(app_private_key_path) as fp:
            alipay_client_config.app_private_key = fp.read()
        with open(alipay_public_key_path) as fp:
            alipay_client_config.alipay_public_key = fp.read()
        # alipay_client_config.app_private_key = '请填写开发者私钥去头去尾去回车，单行字符串'
        # alipay_client_config.alipay_public_key = '请填写支付宝公钥，单行字符串'
        self.client = DefaultAlipayClient(alipay_client_config, logger)

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        # biz_content = {
        #     "subject": subject,
        #     "out_trade_no": out_trade_no,
        #     "total_amount": total_amount,
        #     "product_code": "FAST_INSTANT_TRADE_PAY",
        #     # "qr_pay_mode":4
        # }

        # biz_content.update(kwargs)
        # data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        # return self.sign_data(data)
        """
            页面接口示例：alipay.trade.page.pay
        """
        # 对照接口文档，构造请求对象
        model = AlipayTradePagePayModel()
        model.out_trade_no = "pay201805020000226"
        model.total_amount = 50
        model.subject = "测试"
        model.body = "支付宝测试"
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        settle_detail_info = SettleDetailInfo()
        settle_detail_info.amount = 50
        settle_detail_info.trans_in_type = "userId"
        settle_detail_info.trans_in = "2088302300165604"
        settle_detail_infos = list()
        settle_detail_infos.append(settle_detail_info)
        settle_info = SettleInfo()
        settle_info.settle_detail_infos = settle_detail_infos
        model.settle_info = settle_info
        sub_merchant = SubMerchant()
        sub_merchant.merchant_id = "2088301300153242"
        model.sub_merchant = sub_merchant
        request = AlipayTradePagePayRequest(biz_model=model)
        # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
        response = self.client.page_execute(request, http_method="POST")
        print("alipay.trade.page.pay response:" + response)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        # ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)
