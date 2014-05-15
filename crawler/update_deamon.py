from crawler import monitor
from crawler.models import Item
import time
import threading

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


def update():
    items = Item.objects.all()
    num = 0
    l = len(items)
    while (num < l):
        update_t = UpdateThread(items[num:num+10])
        update_t.start()
        num = num + 10


if __name__ == '__main__':
    while True:
        update()
        time.sleep(7200)
