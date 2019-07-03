#-*- encoding: utf-8 -*-
'''
find_city_name.py
Created on 2019/7/3 15:14
Copyright (c) 2019/7/3, 大战南瓜版权所有.
@author: 大战南瓜
'''

from configs.config import _CITY_CODE

def find_city_name(city_code):
    return list(_CITY_CODE.keys())[list(_CITY_CODE.values()).index(city_code)]