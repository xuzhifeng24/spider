# -*- coding:utf-8 -*-
# @Time    : 2018/5/9 14:56
# @File    : seleniumDemo.py
import requests
import re
from bs4 import BeautifulSoup
import threading
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
import hashlib

class SpiderDemo(object):
    def __init__(self,main_url):
        self.main_url = main_url
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            "Referer":"http://huaban.com/boards/favorite/beauty"
        }

    def set_url(self):
        data = {
            "jgyr75x7":'',
            "max": "28023241",
            "limit": "20",
            "wfl": "1"
        }
        url = "http://huaban.com/boards/favorite/beauty?"+urlencode(data)

        try:
            response = requests.get(url,headers = self.headers)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                self.parse_url(response.text)
            else:
                print("地址解析出错，请重试！")
        except RequestException as e:
            if e == None:
                pass
            else:
                pass

    def parse_url(self,data):
        url_list = []
        content = re.findall(re.compile(r'\"board_id\":([0-9]*),'),data)
        content = set(content)
        for i in content:
            url_list.append("http://huaban.com/boards/{}/".format(i))
        print(url_list)


spider = SpiderDemo("http://huaban.com/boards/favorite/beauty")
print(spider.set_url())