from django.shortcuts import render
import requests
import re
import time
from models import *
from django.db.utils import IntegrityError


# Create your views here.

def get_api_key():
    r = requests.get('https://www.flickr.com/explore')
    key = re.findall('root.YUI_config.flickr.api.site_key = "(\w+)"', r.text)[0]
    return key


def get_photo_list(key):
    r = requests.get('https://api.flickr.com/services/rest?per_page=500&page=1&method=flickr.interestingness.getList'
                     '&extras=url_c%%2Curl_f%%2Curl_h%%2Curl_k%%2Curl_l%%2Curl_m%%2Curl_n%%2Curl_o%%2Curl_q%%2Curl_s'
                     '%%2Curl_sq%%2Curl_t%%2Curl_z'
                     '&api_key=%s&format=json&nojsoncallback=1' % key)
    obj = r.json()
    count = 0
    photos = obj['photos']['photo']
    for i in photos:
        # largest size
        for j in ['o', 'k', 'h', 'l', 'c', 'z', 'm', 'n', 's', 't', 'q', 'sq']:
            if 'url_' + j in i:
                url = i['url_' + j]
                try:
                    item = FlickrItem(pid=long(i['id']), size=j, link=url)
                    item.save()
                    count += 1
                except IntegrityError:
                    pass

    print '[%s] items add %i/%i' % (time.asctime(), count, len(photos))


def scan(request):
    key = get_api_key()
    get_photo_list(key)
