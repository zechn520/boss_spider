#-*- encoding: utf-8 -*-
'''
config.py
Created on 2019/6/24 9:29
Copyright (c) 2019/6/24, 南瓜版权所有.
@author: 大战南瓜
'''

#日志地址
_LOG_DIR = '/tmp/python/cralwer/log/%s'

#数据地址
_LOCAL_DATA_DIR = '/tmp/python/cralwer/data/%s'


_QUEUE_ZECHN = {'NAME':'zechn', 'P_SLEEP_TIME': 2, 'C_MAX_NUM': 3,
                 'C_MAX_SLEEP_TIME': 1, 'C_RETRY_TIMES':3, 'MAX_FAIL_TIMES': 6,
                 'LIMIT_NUM': 2}

#数据库配置_测试
_ZECHN_DB = {'HOST':'localhost', 'USER':'root', 'PASSWD':'root', 'DB':'spider', 'CHARSET':'utf8', 'PORT':3306}


#BOSS直聘配置
_JOB_KEYS= {'大数据','hadoop','spark','etl'}


_CITY_NAME = {'北京'}


_CITY_CODE = {'南京':'c101190100','长沙':'c101250100','东莞':'c101281600','宁波':'c101210400','厦门':'c101230200',
              '成都':'c101270100','重庆':'c101040100','佛山':'c101280800','合肥':'c101220100','天津':'c101030100',
              '西安':'c101110100','苏州':'c101190400','武汉':'c101200100','郑州':'c101180100','北京':'c101010100',
              '上海':'c101020100','深圳':'c101280600','广州':'c101280100','杭州':'c101210100','珠海':'c101280700'
              }