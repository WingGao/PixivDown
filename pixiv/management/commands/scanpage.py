# coding=utf-8
import httplib
import re
import time, json, django, sys, socket, os
import urllib2
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pixiv.models import *
from bs4 import BeautifulSoup

WORK_R18 = 0
WORK_DRANK = 1
out = sys.stdout.write


def get_opener():
    o = urllib2.build_opener()
    o.addheaders = [('Cookie', get_config().get(CONFIG_KEY_COOKIE))]
    return o


def get_time_str():
    return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())


def get_page(opener, link):
    print 'get link ' + link
    res = opener.open(link)
    try:
        html = res.read()
    except httplib.IncompleteRead as e:
        html = e.partial

    obj = json.loads(html)
    try:
        return [i['illust_id'] for i in obj['contents']]
    except:
        return None


def get_page_new(opener, link):
    print 'get link ' + link
    res = opener.open(link)
    try:
        html = res.read()
    except httplib.IncompleteRead as e:
        html = e.partial
    try:
        soup = BeautifulSoup(html)
        divs = soup.select(".work")
        links = [i['href'] for i in divs]
        ids = [i.split('=')[-1] for i in links]
        return ids
    except:
        return None


def save_ids(ids, stype):
    count = 0
    for id in ids:
        item = Item(pid=int(id), type=stype)
        try:
            item.save()
            count += 1
        except django.db.utils.IntegrityError:
            # illute 18 rank item need update from new
            if stype == Item.ILLUTE_18:
                oitem = Item.objects.get(pid=int(id))
                if oitem.type != Item.ILLUTE_18:
                    oitem.type = Item.ILLUTE_18
                    oitem.save()
                    count += 1
    print '[%s] items add %i' % (time.asctime(), count)


def is_cookie_expire():
    t = time.strptime(get_config().get(CONFIG_KEY_COOKIE_EXPIRE), '%Y-%m-%d')
    return (time.mktime(t) - time.mktime(time.gmtime())) / 60 / 60 / 24 < 1


def get_big_link(item):
    if item.big_link is None:
        maxtime = 1
        etime = 0
        while etime <= maxtime:
            try:
                # time.sleep(3)
                opener = urllib2.build_opener()
                opener.addheaders = [('Cookie', get_config().get(CONFIG_KEY_COOKIE)),
                                     ('Referer', item.get_referer_link())]
                res = opener.open(item.get_big_link(), timeout=30)
                imglink = re.findall('<img.*?"(.*?)"', res.read())
                if len(imglink) > 0:
                    item.big_link = imglink[0]
                else:
                    item.big_link = Item.DELETE
                break
            except urllib2.HTTPError, e:
                print e, item.get_big_link()
                if e.code < 400:
                    etime += 1
                else:
                    item.big_link = Item.DELETE
                    break
            except socket.timeout:
                print 'time_out: retry %i' % etime
                etime += 1
                item.big_link = Item.DELETE

        item.save()
    return item.big_link


def download_img(item):
    maxtime = 1
    time = 0
    while time <= maxtime:
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('Cookie', get_config().get(CONFIG_KEY_COOKIE)), ('Referer', item.big_link)]
            res = opener.open(item.big_link)
            if item.type == Item.ILLUTE:
                path = os.path.join(settings.DOWNLOAD_PATH, 'pt')
            elif item.type == Item.ILLUTE_18:
                path = os.path.join(settings.DOWNLOAD_PATH, 'r')
            with open(os.path.join(path, 'pixiv_' + item.get_filename()), 'wb') as f:
                f.write(res.read())
            # 跳出循环
            return True
        except urllib2.HTTPError, e:
            print 'HTTPError: ' + item[2]
            if e.code != 404:
                raise
            else:
                return True
        except socket.timeout:
            print 'time_out: retry %i' % (time)
        # except Exception, e:
        #     print 'DownError:', item.pid, e
        finally:
            time += 1
    return False


def do_scan(mode, content, stype):
    for i in range(1, 11):
        ids = get_page(get_opener(),
                       'http://www.pixiv.net/ranking.php?format=json&mode=%s&content=%s&p=%i' % (
                           mode, content, i))
        if ids is not None:
            save_ids(ids, stype)
        time.sleep(3)


def do_scan_new(mode, stype):
    for i in range(1, 6):
        ids = get_page_new(get_opener(), 'http://www.pixiv.net/%s.php?p=%i' % (mode, i))
        if ids is not None:
            save_ids(ids, stype)
        time.sleep(3)


#
# def build_ef2_string(item):
#     return "<\n%s\nreferer: %s\n>"%(item.big_link,)
def do_download(dtype):
    items = Item.objects.filter(is_download=False)
    count = 0
    if dtype == 1:
        for item in items:
            # print '[%s] Parse %i [%i/%i]' % (time.asctime(), item.pid, count, items.count())
            count += 1
            get_big_link(item)
            if item.big_link == Item.DELETE:
                print '[%s] DELETE %i [%i/%i]' % (time.asctime(), item.pid, count, items.count())
                item.is_download = True
                item.save()
            elif download_img(item):
                print '[%s] Download %i [%i/%i]' % (time.asctime(), item.pid, count, items.count())
                item.is_download = True
                item.save()
    elif dtype == 2:
        print '[%s] Exporting Pixiv pt [%i]' % (time.asctime(), items.count())
        t = get_time_str()
        if items.count() == 0:
            return
        f_pt = open(os.path.join(settings.DOWNLOAD_PATH, 'pixiv_pt_export_%s.txt' % t), 'wb')
        f_r = open(os.path.join(settings.DOWNLOAD_PATH, 'pixiv_r_export_%s.txt' % t), 'wb')
        f_r_new = open(os.path.join(settings.DOWNLOAD_PATH, 'pixiv_r_new_export_%s.txt' % t), 'wb')
        for item in items:
            count += 1
            get_big_link(item)
            if item.big_link != Item.DELETE:
                if item.type == Item.ILLUTE:
                    f_pt.writelines(item.big_link + '\n')
                elif item.type == Item.ILLUTE_18:
                    f_r.writelines(item.big_link + '\n')
                elif item.type == Item.ILLUTE_18_NEW:
                    f_r_new.writelines(item.big_link + '\n')
            item.is_download = True
            item.save()
            print '[%s] Exporting Pixiv %i [%i/%i]' % (time.asctime(), item.pid, count, items.count())
        f_pt.close()
        f_r.close()
        f_r_new.close()


class Command(BaseCommand):
    # D:\GitHub\PixivDown\manage.py scanpage illust
    args = '[illust, illust_18,illust_18_new, download, export]'
    help = 'scan the page'

    def handle(self, *args, **options):
        a1 = args[0]

        if is_cookie_expire():
            print 'cookie expired'
            return

        if a1 == 'illust':
            stype = Item.ILLUTE
            mode = 'daily'
            content = 'illust'
            do_scan(mode, content, stype)
        elif a1 == 'illust_18':
            stype = Item.ILLUTE_18
            mode = 'daily_r18'
            content = 'illust'
            do_scan(mode, content, stype)
        elif a1 == 'illust_18_new':
            stype = Item.ILLUTE_18_NEW
            mode = 'new_illust_r18'
            do_scan_new(mode, stype)
        elif a1 == 'download':
            do_download(1)
        elif a1 == 'export':
            do_download(2)
        else:
            return
