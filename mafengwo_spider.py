# -*- coding:utf-8 -*-
# @Time    : 2018/8/3 9:50
# @File    : mafengwo_spider.py
from query import req
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from 信息爬虫.马蜂窝.get_view import get_json_page
from 信息爬虫.马蜂窝.get_hotel import get_allcity

def input_city():
    print("输入要查询的城市：")
    city = input()
    data = {
        "q":city,
        "t":"mdd",
        "seid":"F2D12C42-3811-4E9F-AAE7-121E9F9FE148"
    }
    url = "http://www.mafengwo.cn/search/s.php?" + urlencode(data)
    resp = req.get_html_content(url)
    bs = BeautifulSoup(resp, "lxml")
    s = bs.find_all("div", attrs={"class": "lst-nub"})[0].find_all("a")
    url1 = s[1]['href']
    url2 = s[2]['href']
    url3 = s[3]['href']
    url4 = s[4]['href']
    iMddid = str(url1).split("/")[-2]
    print("选择要查询的具体内容：1、所有景点 2、酒店 3、机场+酒店 4、当地游")
    c = int(input())
    if c == 1:
        get_json_page(iMddid)
    elif c == 2:
        get_allcity(url2)
    elif c == 3:
        pass
    else:
        pass

def main():
    input_city()

if __name__ == "__main__":
    main()