# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib,urllib2
import re

proxylist = [
            '42.120.22.25:3128',
            '42.121.28.111:3128',
            '42.121.105.155:8888',
            '42.121.105.191:80',
            '111.1.32.51:8080',
            '111.1.36.21:80',
            '111.1.36.23:80',
            '111.1.36.24:80',
            '111.1.36.24:81',
            '111.1.36.24:82',
            '111.1.36.24:84',
            '111.1.36.25:80',
            '111.1.36.25:83',
            '111.1.36.26:80',
            '111.1.36.27:80',
            '111.1.36.27:81',
            '111.1.36.27:82',
            '111.1.36.27:83',
            '111.1.36.27:84',
            '111.1.36.27:85',
            '111.1.36.133:80',
            '111.1.36.137:80',
            '111.1.36.138:80',
            '111.1.36.139:80',
            '111.1.36.140:80',
            '111.1.36.163:80',
            '111.1.36.165:80',
            '111.1.36.166:80',
            '111.1.36.166:81',
            '111.1.36.166:82',
            '111.1.36.166:83',
            '111.1.36.166:84',
            '111.1.55.19:8080',
            '111.1.60.210:80',
            ]
num = 0

class GoodList(object):
    """goods list"""
    def __init__(self):
        super(GoodList, self).__init__()


def amazon(keyword):
    keyworde = urllib.quote(keyword.encode("utf-8"))
    global num
    num = num + 1
    num = num % 34
    proxies = {'http:': proxylist[num]}

    opener = urllib.FancyURLopener(proxies)
    html = opener.open('http://www.amazon.cn/s/ref=nb_sb_noss?field-keywords='+keyworde).read()
    soup = BeautifulSoup(html)
    good_list = soup.find_all(id = re.compile("result_"))
    lists = []
    if len(good_list):
        for item in good_list:
            items = GoodList()
            img = item.find("img")
            title = item.find(attrs={'class':"productTitle"})
            price = item.find(attrs={'class':"newPrice"})
            if price is not None:
                items.img = img['src']
                items.href = title.a['href']
                items.title = title.a.contents[0].encode('utf-8').strip()
                items.price = price.span.get_text()
                lists.append(items)
    lists = lists[0:(len(lists)-3)/4*4+3]
    return lists


def dangdang(keyword):
    keyworde = urllib.quote(keyword.encode("gbk"))
    request = urllib2.Request('http://search.dangdang.com/?key='+keyworde)
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0 FirePHP/0.7.4')
    html = urllib2.urlopen(request).read()
    soup = BeautifulSoup(html,from_encoding="gb18030")
    good_list = soup.find_all("li",attrs={'class':re.compile("line")})
    lists = []
    if len(good_list):
        for item in good_list:
            items = GoodList()
            img = item.find("img")
            title = item.find(attrs={'class':"name"})
            price = item.find(attrs={'class':"price"})
            items.img = img['src']
            items.href = title.a['href']
            items.title = title.a.get_text().encode('utf-8').strip()
            items.price = price.span.get_text()
            pos = items.price.find('-')
            if pos != -1:
                items.price = items.price[0:pos]
            lists.append(items)
    lists = lists[0:(len(lists)-3)/4*4+3]
    return lists


def jd(keyword):
    keyworde = urllib.quote(keyword.encode("utf-8"))
    html = urllib2.urlopen('http://search.jd.com/Search?keyword='+keyworde+'&enc=utf-8&suggest=0').read()
    soup = BeautifulSoup(html)
    good_list = soup.find_all(attrs={'class':"lh-wrap"})
    lists = []
    if len(good_list):
        for item in good_list:
            items = GoodList()
            img = item.find("img")
            title = item.find(attrs={'class':"p-name"})
            price = item.find(attrs={'class':"p-price"})
            items.img = img['data-lazyload']
            items.href = title.a['href']
            items.title = title.a.get_text().encode('utf-8').strip()
            items.price = price.get_text()
            lists.append(items)
    lists = lists[0:(len(lists)-3)/4*4+3]
    return lists


def yhd(keyword):
    keyworde = urllib.quote(keyword.encode("utf-8"))
    html = urllib2.urlopen('http://search.yhd.com/s2/c0-0/k'+keyworde).read()
    soup = BeautifulSoup(html)
    good_list = soup.find_all(attrs={'class':"search_item"})
    lists = []
    if len(good_list):
        for item in good_list:
            items = GoodList()
            img = item.find("img")
            title = item.find(attrs={'class':"title"})
            price = item.find(attrs={'class':"pricebox"})
            if len(img['src']) > 0:
                items.img = img['src']
            else:
                 items.img = img['original']
            items.href = title.a['href']
            items.title= title.a['title'].encode('utf-8').strip()
            items.price = price.span['yhdprice']
            lists.append(items)
    lists = lists[0:(len(lists)-3)/4*4+3]
    return lists


def taobao(keyword):
    keyworde = urllib.quote(keyword.encode("gbk"))
    html = urllib2.urlopen('http://s.taobao.com/search?initiative_id=staobaoz_20140328&js=1&style=grid&q='+keyworde+'&stats_click=search_radio_all%3A1').read()
    soup = BeautifulSoup(html)
    good_list = soup.find_all(attrs={'class':"item-box"})
    lists = []
    if len(good_list):
        for item in good_list:
            items = GoodList()
            img = item.find("img")
            title = item.find(attrs={'class':"summary"})
            price = item.find(attrs={'class':"col price"})
            items.img = img['data-ks-lazyload']
            items.href = title.a['href']
            items.title = title.a.get_text().encode('utf-8').strip()
            items.price = price.get_text()
            lists.append(items)
    lists = lists[0:(len(lists)-3)/4*4+3]
    return lists
