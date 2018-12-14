# -*- coding:utf-8 -*-
# @Time    : 2018/7/27 8:53
# @File    : qunar_spider.py
from bs4 import BeautifulSoup
import re,math,time
from urllib.parse import urlencode
from query import req


def get_page_info():
    data = {
        "hotelSeq": "shenzhen_12785",
        "_": "1532654849335"
    }
    base_url = "http://hotel.qunar.com/render/listOtherSixHeadImage.jsp?" + urlencode(data)
    # resp = req.get_html_content(base_url)
    # bs = BeautifulSoup(resp,"lxml")
    # s = bs.find_all("div",class_="item_hotel_info")
    # print(bs)
    print(base_url)

def main():
    get_page_info()

if __name__ == "__main__":
    main()