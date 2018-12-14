# -*- coding:utf-8 -*-
# @Time    : 2018/8/5 16:31
# @File    : lianjia_spider.py
from bs4 import BeautifulSoup
import pandas as pd
import req


def save_info():
    total_info = []
    for i in range(1,101):
        href = "https://bj.lianjia.com/ershoufang/pg{}/".format(i)
        page_info = parser_html(href)
        total_info = total_info + page_info
    df = pd.DataFrame(data=total_info, columns=['xiaoqu', 'huxing', 'mianji', 'chaoxiang', 'zhuangxiu', 'dianti'])
    df.to_csv('lianjia_house.csv', index=False)
    print('已保存为csv文件.')


def parser_html(href):
    resp = req.get_html_content(href)
    bs = BeautifulSoup(resp,"lxml")
    s = bs.find_all("div",class_="houseInfo")
    house_info = []
    for i in s:
        page_info = []
        try:
            xiaoqu = str(i.text).split("/")[0]
        except:
            xiaoqu = "无"
        page_info.append(xiaoqu)
        try:
            huxing = str(i.text).split("/")[1]
        except:
            huxing = "无"
        page_info.append(huxing)
        try:
            mianji = str(i.text).split("/")[2]
        except:
            mianji = 0
        page_info.append(mianji)
        try:
            chaoxiang = str(i.text).split("/")[3]
        except:
            chaoxiang = "无"
        page_info.append(chaoxiang)
        try:
            zhuangxiu = str(i.text).split("/")[4]
        except:
            zhuangxiu = "无"
        page_info.append(zhuangxiu)
        try:
            dianti = str(i.text).split("/")[5]
        except:
            dianti = "无"
        page_info.append(dianti)
        house_info.append(page_info)
    return house_info

def main():
    save_info()

if __name__ == "__main__":
    main()