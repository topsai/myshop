#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@Time :    2019/11/21 23:07
@Author:  "范斯特罗夫斯基" John
@File: cart.py
@Software: PyCharm
"""
from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:

    def __init__(self, request):
        print('car init')
        """
        初始化购物车对象
        """
        print('初始化购物车')
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 向session中存入空白购物车数据
            print('向session中存入空白购物车数据')
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        print('初始化购物车结束')

    def add(self, product, quantity=1, update_quantity=False):
        print('car add')
        """
        向购物车中增加商品或者更新购物车中的数量
        """

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        print('car save')
        # 设置session.modified的值为True，中间件在看到这个属性的时候，就会保存session
        self.session.modified = True

    def remove(self, product):
        print('car remove')
        """
        从购物车中删除商品
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        print('car iter')
        """
        遍历所有购物车中的商品并从数据库中取得商品对象
        """
        product_ids = self.cart.keys()
        # 获取购物车内的所有商品对象
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        print('car len')
        """
        购物车内一共有几种商品
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        print('car get_total_price', self.cart.values())
        from decimal import getcontext
        d_context = getcontext()
        print(d_context)
        from decimal import InvalidOperation

        for item in self.cart.values():
            print(item['price'], item['quantity'])
            print(Decimal(item['price']) * item['quantity'])
        try:
            e = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        except InvalidOperation as e:
            print(e)
        print(type(e))
        return e

    def clear(self):
        print('car clear')
        del self.session[settings.CART_SESSION_ID]
        self.save()
