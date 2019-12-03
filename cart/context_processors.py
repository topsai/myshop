#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/11/21 23:52
@Author:  "范斯特罗夫斯基" John
@File: context_processors.py
@Software: PyCharm
"""
from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}
