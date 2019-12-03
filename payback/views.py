#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/11/22 0:27
@Author:  "范斯特罗夫斯基" John
@File: urls.py
@Software: PyCharm
"""
from django.shortcuts import render

# Create your views here.
import time
from urllib.parse import parse_qs
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')

# 实例化客户端
alipay_client_config = AlipayClientConfig(sandbox_debug=True)
alipay_client_config.app_id = settings.APPID
with open(settings.APP_PRIVATE) as f:
    alipay_client_config.app_private_key = f.read()
with open(settings.ALIPAY_PUBLIC) as f:
    alipay_client_config.alipay_public_key = f.read()
ALIPAY_client = DefaultAlipayClient(alipay_client_config, logger)


# 创建支付宝订单
def create_trade(price, trade_no, buyer_id="1", subject="商品名"):
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
        response_url = ALIPAY_client.page_execute(request, http_method="GET")
    except Exception as e:
        response_url = None
        print('err', e)
    return response_url


@csrf_exempt
def index(request):
    if request.method == "GET":
        return render(request, 'index.html')
    price = request.POST.get("price")
    import datetime
    no = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    print(no, type(no))
    response_url = create_trade(price, no, '2')
    if response_url:
        return redirect(response_url)


@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
    if request.method == 'POST':
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        alipay = aliPay()

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 1.修改订单状态
            out_trade_no = post_dict.get('out_trade_no')
            print(out_trade_no)
            # 2. 根据订单号将数据库中的数据进行更新
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')
    return HttpResponse('')


@csrf_exempt
def pay_result(request):
    """
    支付完成后，跳转回的地址
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None)

    alipay = aliPay()

    status = alipay.verify(params, sign)

    if status:
        return HttpResponse('支付成功')
    return HttpResponse('支付失败')
