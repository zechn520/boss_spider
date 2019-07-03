#-*- encoding: utf-8 -*-
'''
get_html_util.py
Created on 2019/6/30 20:51
Copyright (c) 2019/6/30, 大战南瓜版权所有.
@author: 大战南瓜
'''
# 使用代理获取html

import requests

def get_proxy():
    return requests.get("http://118.24.52.95:5010/get/").content

def get_html(url):
    # ....

    proxy = get_proxy()
    html = requests.get(url, proxies={"http": "http://{}".format(proxy)})
    return html


url = 'https://www.zhipin.com//job_detail/812f134ba6d228021nx-3NS_FVc~.html'


html = get_html(url)

print html
