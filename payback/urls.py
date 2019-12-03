#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/11/22 0:27
@Author:  "范斯特罗夫斯基" John
@File: urls.py
@Software: PyCharm
"""
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'orders'

urlpatterns = [
    url('', views.index),  #
    url('getway', views.pay_result),  # 支付宝处理完成后回调的get请求路由
    url('back/', views.update_order),  # 支付宝处理完成后回调的post请求路由
]
