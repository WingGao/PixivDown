import re
from django.db import models
from PyEasySetting import PyEasySettingJSON

CONFIG_KEY_COOKIE = 'cookie'
CONFIG_KEY_COOKIE_EXPIRE = 'cookie_expire'

def get_config():
    return PyEasySettingJSON('config.json')

def get_link_id(link):
    # member_illust.php?mode=medium&amp;illust_id=43352503&amp;uarea=daily&amp;ref=rn-b-1-thumbnail-3
    return re.findall('illust_id=(\d+)', link)[0]


class Item(models.Model):
    ILLUTE = 'il'
    ILLUTE_18 = 'il18'
    ILLUTE_18_NEW = 'ni18'
    TYPE_CHOICE = ((ILLUTE, 'illute'), (ILLUTE_18, 'illute_18'), (ILLUTE_18_NEW, 'illute_18_new'))
    DELETE = 'DELETE'
    pid = models.IntegerField(unique=True, db_index=True)
    type = models.CharField(max_length=4, choices=TYPE_CHOICE)
    is_download = models.BooleanField(default=False)
    big_link = models.URLField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def get_referer_link(self):
        # Referer:http://www.pixiv.net/member_illust.php?mode=medium&illust_id=43352503
        return 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%i' % self.pid

    def get_big_link(self):
        return 'http://www.pixiv.net/member_illust.php?mode=big&illust_id=%i' % self.pid

    def get_filename(self):
        return self.big_link.split('/')[-1].split('?')[0]

    def to_ef2(self):
        return '<\n' + self.big_link
