# coding=utf-8
import httplib
import re
import time, json, django, sys, socket, os
import urllib2
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from flickr.models import *
import flickr.views as view


def get_time_str():
    return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())


def do_download(dtype):
    items = FlickrItem.objects.filter(is_download=False)
    count = 0
    if dtype == 1:
        for i in items:
            count += 1
            if dtype == 1:
                print '[%s] Downloading %s [%i/%i]' % (time.asctime(), i.link, count, items.count())
                if download_img(i):
                    i.is_download = True
                    i.save()
    elif dtype == 2:
        print '[%s] Exporting [%i]' % (time.asctime(), items.count())
        if items.count() > 0:
            with open(os.path.join(settings.DOWNLOAD_PATH, 'flickr_export_%s.txt' % get_time_str()),
                      'wb') as f:
                for i in items:
                    f.writelines(i.link.replace('https://', 'http://') + '\n')
                    i.is_download = True
                    i.save()
        print '[%s] Export finish ' % time.asctime()


def download_img(item):
    maxtime = 1
    time = 0
    while time <= maxtime:
        try:
            if False:
                opener = urllib2.build_opener(settings.PROXY)
            else:
                opener = urllib2.build_opener()
            url = item.link.replace('https://', 'http://')
            res = opener.open(url)
            path = os.path.join(settings.DOWNLOAD_PATH, 'flickr')
            with open(os.path.join(path, "flickr_%s" % item.get_filename()), 'wb') as f:
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
        # print 'DownError:', item.pid, e
        finally:
            time += 1
    return False


class Command(BaseCommand):
    # D:\GitHub\PixivDown\manage.py flickr scan
    args = '[scan, download, export]'
    help = 'flickr.com'

    def handle(self, *args, **options):
        a1 = args[0]
        if a1 == 'scan':
            view.scan(None)
        elif a1 == 'download':
            do_download(1)
        elif a1 == 'export':
            do_download(2)
            pass
