#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/12/2 17:51
@Author:  "范斯特罗夫斯基" John
@File: alipay.py
@Software: PyCharm
"""
import logging
from urllib.parse import parse_qs
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')


class Alipay:
    # 初始化支付宝客户端
    def __init__(self):
        alipay_client_config = AlipayClientConfig(sandbox_debug=True)
        alipay_client_config.app_id = settings.APPID
        # 打开 APP_PRIVATE 证书
        with open(settings.APP_PRIVATE) as f:
            alipay_client_config.app_private_key = f.read()
        # 打开 ALIPAY_PUBLIC 证书
        with open(settings.ALIPAY_PUBLIC) as f:
            alipay_client_config.alipay_public_key = f.read()
        # 创建实例
        self.ALIPAY_client = DefaultAlipayClient(alipay_client_config, logger)

    # 创建支付宝订单
    def create_trade(self, price, trade_no, buyer_id="1", subject="商品名"):
        """
        :param buyer_id: 用户id
        :param price: 商品总价格
        :param trade_no: 唯一订单号
        :param subject: 商品名称
        :return: 支付宝跳转链接地址
        """
        # 构造请求参数对象
        model = AlipayTradeCreateModel()
        # 商家唯一订单号
        model.out_trade_no = trade_no
        # product_code 必须这么写
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        # 订单价格
        model.total_amount = price
        # 商品名称
        model.subject = subject
        # 用户 id
        model.buyer_id = buyer_id
        # return model
        request = AlipayTradePagePayRequest(biz_model=model)
        try:
            # 获得支付宝支付地址
            response_url = self.ALIPAY_client.page_execute(request, http_method="GET")
        except Exception as e:
            response_url = None
            print('err', e)
        return response_url
