# -*- coding:utf-8 -*-
# @Time    : 2018/8/7 11:11
# @File    : lg.py
import requests
import time
from sqlalchemy import create_engine
import pandas as pd
from random import choice
import json
import numpy

# engine=create_engine(#这里填你自己数据库的参数#) # 连接数据库
# dl = pd.read_sql("proxys",engine)

def get_proxy(dl):
    n = choice(range(1, len(dl.index)))
    proxy = {"http":"http://%s:%s" %(dl["ip"][n],dl["port"][n]),
             "https": "http://%s:%s" % (dl["ip"][n], dl["port"][n])}
    return(proxy)

def get_header():
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?px=default&city=%E6%B7%B1%E5%9C%B3&district=%E5%8D%97%E5%B1%B1%E5%8C%BA",
        "X-Requested-With": "XMLHttpRequest",
        "Host": "www.lagou.com",
        "Connection":"keep-alive",
        "Cookie":"user_trace_token=20160214102121-0be42521e365477ba08bd330fd2c9c72; LGUID=20160214102122-a3b749ae-d2c1-11e5-8a48-525400f775ce; tencentSig=9579373568; pgv_pvi=3712577536; index_location_city=%E5%85%A8%E5%9B%BD; SEARCH_ID=c684c55390a84fe5bd7b62bf1754b900; JSESSIONID=8C779B1311176D4D6B74AF3CE40CE5F2; TG-TRACK-CODE=index_hotjob; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1485318435,1485338972,1485393674,1485423558; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1485423598; _ga=GA1.2.1996921784.1455416480; LGRID=20170126174002-691cb0a5-e3ab-11e6-bdc0-525400f775ce",
        "Origin": "https://www.lagou.com",
        "Upgrade-Insecure-Requests":"1",
        "X-Anit-Forge-Code": "0",
        "X-Anit-Forge-Token": "None",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
        }
    return(headers)

def get_form(i):
    data={"first":"false","pn":i,"kd":"数据分析师"}
    return(data)

districts = ["南山区","福田区","宝安区","龙岗区","龙华新区","罗湖区","盐田区","大鹏新区"]
pagenos = [22,10,1,4,1,2,1,1]
url_lists = ["https://www.lagou.com/jobs/positionAjax.json?px=default&city=深圳&district=%s&needAddtionalResult=false"%area for area in districts]

s = requests.Session()
s.keep_alive = False
s.adapters.DEFAULT_RETRIES = 10

def get_jobinfo(i,j): # i表区号，j表页数
    if i >= 8 or j > pagenos[i]:
        return("索引超标！")
    resp=s.post(url_lists[i], data=get_form(j), headers=get_header())
    resp.encoding="utf-8"
    max_num = len(json.loads(resp.text)["content"]["positionResult"]["result"])
    for k in range(max_num):
        try:
            json_data=json.loads(resp.text)["content"]["positionResult"]["result"][k]
            df = pd.DataFrame(dict(
                approve=json_data["approve"],
        #        businessZones=json_data["businessZones"],
                companyId=json_data["companyId"],
        #        companyLabelList=json_data["companyLabelList"],
                companyShortName=json_data["companyShortName"],
                companySize=json_data["companySize"],
                createTime=json_data["createTime"],
                education=json_data["education"],
                financeStage=json_data["financeStage"],
                firstType=json_data["firstType"],
                industryField=json_data["industryField"],
                jobNature=json_data["jobNature"],
                positionAdvantage=json_data["positionAdvantage"],
                positionId=json_data["positionId"],
                positionName=json_data["positionName"],
                salary=json_data["salary"],
                secondType=json_data["secondType"],
                workYear=json_data["workYear"],
                scrapy_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),index=[0])
            df.to_sql(con = engine, name = "job_info", if_exists = 'append', flavor = "mysql",index=False)
        except:
            print("第%d区，第%d页，第%d个出错了！"%(i,j,k))