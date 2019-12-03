#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/11/22 0:27
@Author:  "范斯特罗夫斯基" John
@File: urls.py
@Software: PyCharm
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
]
