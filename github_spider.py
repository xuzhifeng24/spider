# -*- coding: utf-8 -*-
# @Time    : 2018/11/4 14:15
# @Author  : xuzhifeng
# @File    : github_spider.py
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import multiprocessing as mp
import threading as td

os.getcwd()
os.chdir(r'C:\Users\66483\Desktop\h')
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
}


def get_url():
   f = open(r'E:\Python\spider-demo-master\信息爬虫\github下载\bookmarks_2018_11_5.txt',encoding='utf-8')
   content = f.read()
   bs = BeautifulSoup(content,'lxml')
   s = bs.find_all('a')
   for i in s:
       url = i.get('href')
       get_parser(url)

   # threads = []
   # for i in s:
   #     url = i.get('href')
   #
   #     thread = td.Thread(target=get_parser, args=(url,))
   #     thread.start()
   #     threads.append(thread)
   #
   #     for tr in threads:
   #         tr.join()

def get_parser(url):
    response = requests.get(url,headers=headers).text
    bs = BeautifulSoup(response, 'lxml')
    s = bs.find_all('a', class_='btn btn-outline get-repo-btn ')
    path = os.getcwd()
    for i in s:
        href = "https://github.com" + i.get('href')
        try:
            file_name = str(href).split("/")[3] + "_" + str(href).split("/")[4]
            print("正在下载：",file_name)
            f = requests.get(href, headers).content
            if os.path.exists(file_name) == False:
                with open(file_name, "wb") as file:
                    file.write(f)
            else:
                print(file_name, "已存在")
        except ValueError:
            print(href)

# def get_lat_long(url):
#     # driver = webdriver.PhantomJS(executable_path=r'C:\Users\66483\Downloads\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get(url)
#     driver.find_element_by_xpath(r'//*[@id="js-repo-pjax-container"]/div[2]/div[1]/div[4]/details/summary').click()
#     driver.find_element_by_xpath(r'//*[@id="js-repo-pjax-container"]/div[2]/div[1]/div[4]/details/div/div/div[1]/div[2]/a[2]').click()
#     time.sleep(120)  # 延时等待搜索结果
#     driver.close()

get_url()
