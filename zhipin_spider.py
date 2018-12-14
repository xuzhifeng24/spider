# -*- coding:utf-8 -*-
# @Time    : 2018/7/21 15:49
# @File    : Bosszhipin_test.py

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from urllib.parse import urlencode
import re
import pandas as pd
import time
import os
from multiprocessing import Pool,Process
from IP代理池 import read_ip

headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
           }
base_url = 'https://www.zhipin.com/job_detail/?'

def get_proxies():
    proxies = {
        'http': "http://{0}:{1}".format(read_ip.user_ip()['ip'],read_ip.user_ip()['port'])
    }
    return proxies

def input_keyword():
    print("欢迎使用BOSS直聘职位分析系统！")
    keyword = input("请输入要查询的职位：")
    print("\n")
    return keyword

def get_target_link(keyword):
    total_info = []
    for i in range(1,11):
        ka = str("page-{0}".format(i)).replace("\'","\"")
        data ={
           "query": keyword,
            "page": i,
            "ka": ka
        }
        url = base_url + urlencode(data)
        total_info.append(get_target_content(url))

    # df = pd.DataFrame(data=total_info, columns=['job_name', 'job_wage', 'company_location', 'work_experience', 'company'])
    # df.to_csv('boss_job.csv', index=False)
    # print('已保存为csv文件.')
   # print(total_info)

def get_target_content(url):
    try:
        proxies =  get_proxies()
        print(proxies)
        response = requests.get(url = url,headers = headers,proxies = proxies)
        if response.status_code == 200:
            job_info = []
            soup = BeautifulSoup(response.text, "lxml")
            s = soup.find_all("div", class_="job-list")
            for i in s:
                m = i.find_all("li")
                for j in m:
                    job_info.append(j)

            job_infos = []
            job_csvs = []
            for i in job_info:
                s = i.find_all("div", class_="job-primary")
                for j in s:
                    job_name = j.find("div", class_="job-title").get_text()
                    job_csvs.append(job_name)
                    job_wage = j.find("span").get_text()
                    job_csvs.append(job_wage)
                    company_location = re.search(r"([\u4e00-\u9fa5]{2})(\s{2})", str(j).replace("\n", "")).group(1)
                    job_csvs.append(company_location)
                    work_experience = re.search(r"</em>(.*)<em", str(j)).group(1)
                    job_csvs.append(work_experience)
                    m = j.find_all("div", class_="company-text")
                    for k in m:
                        company = k.find("a").get_text()
                        job_csvs.append(company)
                    job_infos.append(job_csvs)
                    print(job_infos)
        else:
            print("shibai")
            #get_target_content(url)

    except RequestException as e:
        print(e)

def main():
    get_target_link(input_keyword())

if __name__ == '__main__':
    main()