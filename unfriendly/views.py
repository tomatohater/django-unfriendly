from urlparse import urlparse

from django.core.urlresolvers import resolve, Resolver404
from django.http import HttpResponse, HttpResponseNotFound, QueryDict

from unfriendly import settings
from unfriendly.utils import Obfuscator


def deobfuscate(request, key, juice=None):
    """
    Returns HttpResponse from original obfuscated view.
    SEO juice is ignored since it is only for URL display purposes.
    """
    obfuscator = Obfuscator(settings.UNFRIENDLY_SECRET)
    try:
        url = obfuscator.deobfuscate(str(key))
    except:
        return HttpResponseNotFound()
    url_parts = urlparse(url)
    path = url_parts.path
    query = url_parts.query

    try:
        view, args, kwargs = resolve(path)
    except Resolver404:
        return HttpResponseNotFound()

    if query:
        request.GET = QueryDict(query)

    return view(request, *args, **kwargs)
