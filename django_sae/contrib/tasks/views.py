# coding=utf-8
from django.http import HttpResponse, Http404


def execute(request, key):
    from django.core.cache import cache

    try:
        o = cache.get(str(key))
        if o is None:
            raise Http404('not exist key: %s' % key)
        else:
            o.execute()
            return HttpResponse('success')
    finally:
        cache.delete(key)