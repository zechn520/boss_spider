#-*- encoding: utf-8 -*-
'''
spider.py
Created on 2019/6/29 22:35
Copyright (c) 2019/6/29, 南瓜版权所有.
@author: 大战南瓜
'''

import requests,datetime,re,time,random
from bs4 import BeautifulSoup
from utils.util import Util
from utils.find_city_name import find_city_name
from utils.db_util import DBUtil
from configs.config import _ZECHN_DB,_CITY_CODE


headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"
}


#找到搜索页的详细链接
def find_detil_urls(city_code,job_key):

    res = []
    db_util = DBUtil(_ZECHN_DB)

    for i in range(1,11):

        print '开始处理%s的%s搜索页结果,目前为第%s页' %(find_city_name(city_code),job_key,i)
        # 需要处理的搜索页url
        url = 'https://www.zhipin.com/%s/?query=%s&page=%s&ka=page-%s' %(city_code,job_key,i,i)
        try:
            html = requests.get(url,headers=headers)
        except:
            print '搜索页解析失败,10min后重试,该页面为:'
            print url
            time.sleep(600)
            html = requests.get(url,headers=headers)
        soup = BeautifulSoup(html.text,'html.parser')

        job_box = soup.find('div','job-box')
        if(job_box is None):
            print '城市:%s的%s岗位搜索结果已经没有了,一共%s页' %(find_city_name(city_code),job_key,i)
            break

        for n in soup.find_all('div', 'job-primary'):
            # res = []
            # res.append(n.find('div', 'job-title').string)  # 添加职位名
            # res.append(n.find('span', 'red').string)  # 添加薪资
            # res.append(n.find('div', 'company-text').find('a').string)  # 添加公司名
            # print json.dumps(res,ensure_ascii=False)
            # print res[0],res[1],res[2]
            detail_url =  'https://www.zhipin.com/'+ n.find('a')['href'] #详细工作网址

            sql = """
            select * from boss_spider where url = '%s';
            """
            url_res = db_util.read_one(sql % detail_url)

            if (url_res == None):
                print '发现新岗位,加入暂存区,岗位链接为:'
                print detail_url
                res.append(detail_url)
            else:
                pass


        if i ==10:
            print '城市:%s的%s岗位搜索页已经没有新岗位了,一共10页' %(find_city_name(city_code),job_key)
        # print '爬完一个搜索页 休息5s左右'
        # t1 = random.uniform(5,10)
        # time.sleep(t1)
    return res

# 处理一页的搜索记录
def add_info_by_urls(urls):

    count = 0
    total_count = 0
    for i in urls:
        print '本次处理的网址是:'
        print i
        try:
            html = requests.get(i,headers=headers)
        except:
            print '处理失败,10分钟后重试'
            time.sleep(10)
            html = requests.get(i,headers=headers)

        soup = BeautifulSoup(html.text,'html.parser')

        job_info = soup.find('div','info-primary')
        try:
            job_title =job_info.find('div','name').find('h1','').text.encode('UTF-8')  #获取工作title
        except:
            print 'ip被限制了,给你60s 手动解冻下'
            time.sleep(60)
            try:
                html = requests.get(i,headers=headers)
            except:
                print '处理失败,10分钟后重试'
                time.sleep(10)
                html = requests.get(i,headers=headers)

            soup = BeautifulSoup(html.text,'html.parser')

            job_info = soup.find('div','info-primary')
            job_title =job_info.find('div','name').find('h1','').text.encode('UTF-8')  #获取工作title



        money = job_info.find('div','name').find('span','salary').text.encode('UTF-8') #获取工资
        job_requirements = job_info.find('p').find_all(text=re.compile('.*'))#
        work_location = ''.join(job_requirements[0]).encode('UTF-8')#工作地点
        work_experience = ''.join(job_requirements[1]).encode('UTF-8') #经验要求
        education = ''.join(job_requirements[2]).encode('UTF-8') #学历要求


        job_box = soup.find('div','job-box')
        jd = job_box.find('div','text').text.encode('UTF-8') #工作描述
        try:
            company_name = job_box.find('div','detail-content').find('div','name').text.encode('UTF-8') #公司名称
            company_type = ''.join(job_box.find('li','company-type').find_all(text=re.compile('.*'))[1]).encode('UTF-8') #公司类型
        except:
            company_name_str = soup.title.text.encode('UTF-8')
            company_name = company_name_str.split('_')[1].split('-')[0]
            company_type = '未知'

        create_times = datetime.datetime.now().date()
        url = i
        util = Util()
        md5_str = job_title+company_name+str(url)
        md5 = util.get_md5(md5_str)


        sql = """
        insert into boss_spider (job_title,company_name,company_type,money,work_location,work_experience,education,jd,url,create_times,md5) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on DUPLICATE KEY UPDATE param = %s;
        """

        count_sql = """
        select param from boss_spider where md5 = %s;
        """

        dbutil = DBUtil(_ZECHN_DB)
        # print count_sql % md5
        spider_count = dbutil.read_one(count_sql,md5)

        if spider_count == None:
            count += 1
            print '有一个新岗位出现呦!'
        else:
            spider_count = spider_count[0]
            spider_count = int(spider_count)+1 #重复爬取次数

        params = [job_title,company_name,company_type,money,work_location,work_experience,education,jd,url,create_times,md5,spider_count]

        try:
            result  = dbutil.execute(sql,params)
        except:
            print '有一条插入失败 url为:'
            print url


        total_count += 1
        if(total_count % 17 == 0):
            print '每爬完17条具体职位数据后休息1s'
            time.sleep(1)


        print '正在处理第%d条职位数据' % total_count
        sleep_time = random.uniform(0,1)
        # print '处理完成,睡眠%s秒,继续爬下一条数据' % sleep_time
        print '..............................................'
        # time.sleep(sleep_time)
    print 'success!一共发现了%d条新职位' %count
