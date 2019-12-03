#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/11/22 0:27
@Author:  "范斯特罗夫斯基" John
@File: forms.py
@Software: PyCharm
"""
from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
