from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext
from django.http import HttpResponseRedirect
from crawler import spider
from crawler import monitor
from crawler.models import Item
from datetime import *
import threading

amazonlist = []
dangdanglist = []
jdlist = []
taobaolist = []
yhdlist = []

class AmazonThread(threading.Thread):
    def __init__(self, keyword):
        self.keyword = keyword
        threading.Thread.__init__(self)

    def run (self):
        global amazonlist
        amazonlist = spider.amazon(self.keyword)



class DangdangThread(threading.Thread):
    def __init__(self, keyword):
        self.keyword = keyword
        threading.Thread.__init__(self)

    def run (self):
        global dangdanglist
        dangdanglist = spider.dangdang(self.keyword)



class JdThread(threading.Thread):
    def __init__(self, keyword):
        self.keyword = keyword
        threading.Thread.__init__(self)

    def run (self):
        global jdlist
        jdlist = spider.jd(self.keyword)



class TaobaoThread(threading.Thread):
    def __init__(self, keyword):
        self.keyword = keyword
        threading.Thread.__init__(self)

    def run (self):
        global taobaolist
        taobaolist = spider.taobao(self.keyword)


class YhdThread(threading.Thread):
    def __init__(self, keyword):
        self.keyword = keyword
        threading.Thread.__init__(self)

    def run (self):
        global yhdlist
        yhdlist = spider.yhd(self.keyword)


class UpdateThread(threading.Thread):
    def __init__(self, items):
        self.items = items
        threading.Thread.__init__(self)

    def run (self):
        for item in self.items:
            if item.types == 'amazon':
                monitor.amazon_update(item)
            elif item.types == 'dangdang':
                monitor.dangdang_update(item)
            elif item.types == 'yhd':
                monitor.yhd_update(item)
            else:
                monitor.taobao_update(item)


def search(request):
    global amazonlist
    global dangdanglist
    global yhdlist
    global taobaolist
    amazonlist = []
    dangdanglist = []
    yhdlist = []
    taobaolist = []
    keyword = request.GET.get("search", "")
    types = request.GET.get("filter", "")
    if types == "all":
        amazon_t = AmazonThread(keyword)
        dangdang_t = DangdangThread(keyword)
        yhd_t = YhdThread(keyword)
        taobao_t = TaobaoThread(keyword)
        amazon_t.start()
        dangdang_t.start()
        yhd_t.start()
        taobao_t.start()
        amazon_t.join()
        dangdang_t.join()
        yhd_t.join()
        taobao_t.join()
    elif types == "amazon":
        amazonlist = spider.amazon(keyword)
    elif types == "dangdang":
        dangdanglist = spider.dangdang(keyword)
    elif types == "yhd":
        yhdlist = spider.yhd(keyword)
    else:
        taobaolist = spider.taobao(keyword)

    return render_to_response('result.html',{'amazonlist':amazonlist, 'dangdanglist':dangdanglist, \
           'yhdlist':yhdlist, 'taobaolist':taobaolist, 'user':request.user})



def track(request):
    if request.user.is_authenticated():
        href = request.GET['hrefs']
        print href
        types = request.GET['col']
        print types
        name = request.GET['names'].strip()
        img = request.GET['img']
        price = request.GET['price'].strip()
        m = str(datetime.today().month)
        if len(m) < 2:
            m = '0' + m
        d = str(datetime.today().day)
        if len(d) < 2:
            d = '0' + d
        dates = m + '.' + d
        if ( (cmp(price[0],'0')<0) or (cmp(price[0],'9')>0) ):
            price = price[1:].strip()
        try:
            Item.objects.get(href=href,user=request.user)
            return HttpResponse(simplejson.dumps({'codes':'ALREADY'}))
        except Item.DoesNotExist:
            item = Item(types=types,href=href,name=name,img=img,user=request.user,prices=price,dates=dates)
            item.save()
            return HttpResponse(simplejson.dumps({'codes':'SUCCESS'}))
    else:
        return HttpResponse(simplejson.dumps({'codes':'LOGIN'}))


def detrack(request,item_id):
    if request.user.is_authenticated():
        try:
            item = Item.objects.get(id=str(item_id))
            item.delete()
            return HttpResponseRedirect("/lists", RequestContext(request))
        except Item.DoesNotExist:
            return HttpResponseRedirect("/lists", RequestContext(request))
    else:
        return HttpResponseRedirect("/login", RequestContext(request))



def lists(request):
    if request.user.is_authenticated():
        items = Item.objects.filter(user=request.user)
        return render_to_response('lists.html',{'items':items,'user':request.user})
    else:
        return render_to_response('login.html',RequestContext(request))



def realupdate(request):
    if request.user.is_authenticated():
        items = Item.objects.filter(user=request.user)
        num = 0
        l = len(items)
        while (num < l):
            update_t = UpdateThread(items[num:num+3])
            update_t.start()
            num = num + 3
        return render_to_response('lists.html',{'items':items,'user':request.user})
    else:
        return render_to_response('login.html',RequestContext(request))


def detail(request,item_id):
    if request.user.is_authenticated():
        try:
            item = Item.objects.get(id=str(item_id))
            prices = item.prices.split(',')
            for i in range(len(prices)):
                prices[i] = float(prices[i])
            dates = item.dates.decode("utf-8").split(',')
            return render_to_response('detail.html',{'item':item,'prices':prices,'dates':dates,'user':request.user})
        except Item.DoesNotExist:
            return HttpResponseRedirect("/lists", RequestContext(request))
    else:
        return HttpResponseRedirect("/login", RequestContext(request))
