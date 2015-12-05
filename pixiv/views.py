from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import models


# Create your views here.
def config_view(request):
    config = models.get_config()
    if request.method == 'GET':
        return render_to_response('config_view.html', {
            'cookie': config.get(models.CONFIG_KEY_COOKIE, ''),
            'cookie_expire': config.get(models.CONFIG_KEY_COOKIE_EXPIRE, ''),
        })
    elif request.method == 'POST':
        config.set({
            models.CONFIG_KEY_COOKIE: request.POST.get('cookie', ''),
            models.CONFIG_KEY_COOKIE_EXPIRE: request.POST.get('cookie_expire', '')
        })
        return HttpResponseRedirect('/config')
