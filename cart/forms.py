#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/11/21 23:11
@Author:  "范斯特罗夫斯基" John
@File: forms.py
@Software: PyCharm
"""
from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
