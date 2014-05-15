# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from datetime import *
import urllib2


def amazon_update(item):
    html = urllib2.urlopen(item.href).read()
    p1 = html.find('特价:')
    if p1 == -1:
        p1= html.find('价格:')
        if (p1 == -1):
            p1 =  html.find('价格：')
    p2= html.find("<td",p1)
    p3= html.find("</td>",p2)
    tt = html[p2:p3+5]
    soup = BeautifulSoup(tt)
    price = soup.get_text().strip()
    if ( (cmp(price[0],'0')<0) or (cmp(price[0],'9')>0) ):
        price = price[1:10].strip()
    else:
        price = price[1:9].strip()
    oldp = item.prices
    oldd = item.dates
    m = str(datetime.today().month)
    if len(m) < 2:
        m = '0' + m
    d = str(datetime.today().day)
    if len(d) < 2:
        d = '0' + d
    dates = m + '.' + d
    prices = item.prices.split(',')
    if prices[-1] != price:
        if (len(prices) < 20):
            oldp = oldp + ',' + price
            oldd = oldd + ',' + dates
        else:
            pos = oldp.find(',')
            oldp = oldp[pos+1:] + ',' + price
            pos = oldd.find(',')
            oldd = oldd[pos+1:] + ',' + dates
        item.prices = oldp
        item.dates = oldd
        item.save()



def dangdang_update(item):
    html = urllib2.urlopen(item.href).read()
    soup = BeautifulSoup(html)
    price = soup.find(attrs={'class':'d_price'}).get_text().strip()
    if ( (cmp(price[0],'0')<0) or (cmp(price[0],'9')>0) ):
        price = price[1:10].strip()
    else:
        price = price[1:9].strip()
    oldp = item.prices
    oldd = item.dates
    m = str(datetime.today().month)
    if len(m) < 2:
        m = '0' + m
    d = str(datetime.today().day)
    if len(d) < 2:
        d = '0' + d
    dates = m + '.' + d
    prices = item.prices.split(',')
    if prices[-1] != price:
        if (len(prices) < 20):
            oldp = oldp + ',' + price
            oldd = oldd + ',' + dates
        else:
            pos = oldp.find(',')
            oldp = oldp[pos+1:] + ',' + price
            pos = oldd.find(',')
            oldd = oldd[pos+1:] + ',' + dates
        item.prices = oldp
        item.dates = oldd
        item.save()




def taobao_update(item):
    url = item.href
    pos = url.find('id=')
    item_id = url[pos+3:pos+14]
    if url.find('tmall') == -1:
        html = urllib2.urlopen('http://tui.taobao.com/recommend?itemid='+item_id+'&appid=39&count=500').read()
        pos = html.find('itemId')
        rec_id = html[pos+8:pos+19]
        html = urllib2.urlopen('http://tui.taobao.com/recommend?itemid='+rec_id+'&appid=39&count=500').read()
        pos = html.find(item_id.encode('utf-8'))
        if pos == -1:
            price = '-1'
        else:
            pos1 = html.find('promotionPrice',pos)
            pos2 = html.find(',',pos1)
            price = html[pos1+16:pos2]
            if price == '0.0':
                pos1 = html.find('price',pos)
                pos2 = html.find(',',pos1)
                price = html[pos1+7:pos2]
    else:
        html = urllib2.urlopen('http://aldcdn.tmall.com/recommend.htm?itemId='+item_id+'&appId=03054&callback=jsonpAld03054').read()
        pos = html.find('id')
        rec_id = html[pos+4:pos+15]
        html = urllib2.urlopen('http://aldcdn.tmall.com/recommend.htm?itemId='+rec_id+'&appId=03054&callback=jsonpAld03054').read()
        pos = html.find(item_id.encode('utf-8'))
        if pos == -1:
            price = '-1'
        else:
            pos1 = html.find('price',pos)
            pos2 = html.find(',',pos1)
            price = html[pos1+7:pos2]

    if price != '-1':
        if ( (cmp(price[0],'0')<0) or (cmp(price[0],'9')>0) ):
            price = price[1:10].strip()
        else:
            price = price[0:9].strip()
        oldp = item.prices
        oldd = item.dates
        m = str(datetime.today().month)
        if len(m) < 2:
            m = '0' + m
        d = str(datetime.today().day)
        if len(d) < 2:
            d = '0' + d
        dates = m + '.' + d
        prices = item.prices.split(',')
        if prices[-1] != price:
            if (len(prices) < 20):
                oldp = oldp + ',' + price
                oldd = oldd + ',' + dates
            else:
                pos = oldp.find(',')
                oldp = oldp[pos+1:] + ',' + price
                pos = oldd.find(',')
                oldd = oldd[pos+1:] + ',' + dates
            item.prices = oldp
            item.dates = oldd
            item.save()



def yhd_update(item):
    html = urllib2.urlopen(item.href).read()
    soup = BeautifulSoup(html)
    price = soup.find(attrs={'class':'price_l'})
    price = price.get_text().strip()
    if ( (cmp(price[0],'0')<0) or (cmp(price[0],'9')>0) ):
        price = price[1:10].strip()
    else:
        price = price[1:9].strip()
    oldp = item.prices
    oldd = item.dates
    m = str(datetime.today().month)
    if len(m) < 2:
        m = '0' + m
    d = str(datetime.today().day)
    if len(d) < 2:
        d = '0' + d
    dates = m + '.' + d
    prices = item.prices.split(',')
    if prices[-1] != price:
        if (len(prices) < 20):
            oldp = oldp + ',' + price
            oldd = oldd + ',' + dates
        else:
            pos = oldp.find(',')
            oldp = oldp[pos+1:] + ',' + price
            pos = oldd.find(',')
            oldd = oldd[pos+1:] + ',' + dates
        item.prices = oldp
        item.dates = oldd
        item.save()

