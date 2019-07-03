#-*- encoding: utf-8 -*-
'''
action.py.py
Created on 2019/6/30 16:04
Copyright (c) 2019/6/30, 南瓜版权所有.
@author: 大战南瓜
'''
import time,datetime
from spider import find_detil_urls,add_info_by_urls

from configs.config import _CITY_CODE,_JOB_KEYS,_CITY_NAME

time1 = datetime.datetime.now()

print '爬虫开始,开始工作时间为:%s' %time1

start_time = time.time()
for job_key in _JOB_KEYS:
    for city_name in _CITY_NAME:
        urls = find_detil_urls(_CITY_CODE[city_name],job_key)
        # print '爬完搜索页休息1s'
        # time.sleep(1)

        add_info_by_urls(urls)
        print '处理完%s的%s所有职位数据,准备进行下一个城市的处理' %(city_name,job_key)
        # print '休息1分钟'
        # time.sleep(60)
end_time = time.time()


t = (end_time-start_time)/60/60

time2 = datetime.datetime.now()

print '爬虫工作完成,结束工作时间为:%s' %time2

print '本次爬虫一共消耗%s小时' % t