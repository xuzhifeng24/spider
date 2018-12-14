# -*- coding:utf-8 -*-
# @Time    : 2018/8/1 21:20
# @File    : tieba_spider.py
import time,re
import multiprocessing as mp
import threading as td
import pymysql
from query import req
from bs4 import BeautifulSoup
from urllib.parse import urlencode

def get_connect():
    config = {
        "user":"root",
        "password":"123456",
        "host":"localhost",
        "charset":"utf8",
        "db":"tieba_db",
        "port":3306
    }
    conn = pymysql.connect(**config)
    return conn

def get_province_allschool(province_school):
    data = {
        "fd": "高等院校",
        "ie":"utf-8",
        "sd": province_school
    }
    url = "http://tieba.baidu.com/f/fdir?" + urlencode(data)
    resp = req.get_html_content(url)
    return resp

def get_allprovince_school():
    resp = get_province_allschool("甘肃院校")
    bs = BeautifulSoup(resp, "lxml")
    s = bs.find_all("div",attrs={"class":"root_dir_box"})[0].find_all("li")
    for i in s[:-2]:
        start_time = time.time()
        try:
            href = "http://tieba.baidu.com" + i.find('a')['href']
            province_name = get_province_name(href)
            print("正在爬取：" + province_name)
            get_page(href)
            over_time = time.time()
            print(province_name + "爬取完毕，用时：" + str(over_time - start_time))
        except:
            print("事故了。。。。。。。。")
            break

def get_province_name(href):
    resp = req.get_html_content(href)
    bs = BeautifulSoup(resp, "lxml")
    return bs.find_all("h2")[1].find("span").text

def get_page(href):
    threads = []
    resp = req.get_html_content(href)
    bs = BeautifulSoup(resp, "lxml")
    s = bs.find_all("div",class_="pagination")[0].find_all('a')[-1]
    page = re.search(r"&amp;pn=([0-9]*)\">尾页</a>",str(s)).group(1)
    pool = mp.Pool(15)
    for i in range(1,int(page)+1):
        link = href +"&pn={}".format(i)
        pool.apply_async(get_province_school,args=(link,))
    pool.close()
    pool.join()

def get_province_school(href):
    resp = req.get_html_content(href)
    bs = BeautifulSoup(resp,"lxml")
    s = bs.find_all("div",attrs={"id":"dir_content_main"})[0].find_all("td")
    for i in s[1:]:
        href = i.find('a')['href']
        parse_html(href)

def parse_html(href):
    resp = req.get_html_content(href)
    bs = BeautifulSoup(resp,"lxml")
    s = bs.find_all("div",attrs={"class":"card_title"})
    for i in s:
        school = str(i.find("a").get_text()).strip().replace("吧","")
        guanzhu = re.search(r'<span class="card_menNum">(.*)</span>',str(i)).group(1)
        tiezi = re.search(r'<span class="card_infoNum">(.*)</span>',str(i)).group(1)
        print(school,"关注：",guanzhu,"帖子：",tiezi)
        conn = get_connect()
        with conn.cursor() as cursor:
            sql = "insert into gz_db(school,guanzhu,tieshu) values(%s,%s,%s)"
            cursor.execute(sql,(school,guanzhu,tiezi))
        conn.commit()
        cursor.close()

def main():
    get_allprovince_school()

if __name__ == "__main__":
    main()