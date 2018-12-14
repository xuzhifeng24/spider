# -*- coding:utf-8 -*-
# @Time    : 2018/4/28 21:49
# @File    : test_01.py

import requests
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import ConnectionError

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie':'SUV=1516185056513745; SMYUV=1516185056513696; UM_distinctid=16103abf734740c-080d5a591-6b12157e-1fa400-16103abf744db7e; CXID=1B381A49571CE6D4A5EF08CBF1C6FA36; SUID=3ECF55DF5D68860A5A66F4590004C528; ad=IZllllllll2zL8yclllllVrb2RklllllNzLV@Zllll9lllllVqxlw@@@@@@@@@@@; IPLOC=CN5101; pgv_pvi=6476657664; pgv_si=s9605117952; ABTEST=4|1524923403|v1; weixinIndexVisited=1; JSESSIONID=aaaYG-g6ADNMYbKhQhlmw; ppinf=5|1524923554|1526133154|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlQkYlOTclRTklOTQlOEJ8Y3J0OjEwOjE1MjQ5MjM1NTR8cmVmbmljazoxODolRTUlQkYlOTclRTklOTQlOEJ8dXNlcmlkOjQ0Om85dDJsdURaR254WThKZ0E4ZU1Vb2ptSEU4TzBAd2VpeGluLnNvaHUuY29tfA; pprdig=mWa7mBvqmhW6ZulnT9dtJVWjAlJO7jwK3T7ustK9CN8cUv7DJPT-ISpGjv22RYMAvvtSZLjSN6ykrg6L1Ejyr-wd1sfqXyuozKuIBHqKftcH8259KY4aUSJR_5zc_QskoaR-BQMGOY2y4OxuPacfbrc8gwrb8nQX_QnovW44mn0; sgid=02-32670561-AVrkfKKvJFoAfXictroKsKms; ppmdig=15249235540000009f81d7e02be48d283d9cd602ae121ad2; PHPSESSID=9r5lgqj3ir1i5kq8a3omradia2; SUIR=5B034A90E6E38F0D032160F9E6C8ECF2; sct=2; ld=Hkllllllll2zi4TmlllllVr6KWclllllNz8Osyllll9lllll4llll5@@@@@@@@@@; LSTMV=245%2C74; LCLKINT=2452; SNUID=EDAAFC2550553AB94CC92E795009BF29; seccodeRight=success; successCount=2|Sat, 28 Apr 2018 13:59:26 GMT',
    'Host':'weixin.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
}
keywords = "风景"
proxy_pool_url = 'http://127.0.0.1:5000/get'

proxy = None

def get_proxy():
    try:
        response =  requests.get(proxy_pool_url)
        if response.status_code ==200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url):
    print("Crawling",url)
    global proxy
    try:
        # 有代理的情况
        if (proxy== None) == False:
            proxies = {
                'http':'http://'+proxy
            }
            response = requests.get(url, allow_redirects=False,headers = headers,proxies = proxies)

        # 无代理的情况
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)

        if response.status_code == 200:
            return response.text

        if response.status_code ==302:
            #需要代理
            print('iP被封，正在抓取代理！')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy:',proxy)
                return get_html(url)
            else:
                print("Get Proxy Faild")

    except ConnectionError as e:
        print("Error Occurred",e.args)
        proxy = get_proxy()
        return get_html(url)


def get_index(keyword,page):
    data = {
        'query' : keyword,
        'type':2,
        'page':page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def main():
    for page in range(1,101):
        html = get_index(keywords,page)
        print(html)

if __name__ == '__main__':
    main()