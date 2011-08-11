from urlparse import urlparse

from django.core.urlresolvers import resolve, Resolver404
from django.http import HttpResponse, HttpResponseNotFound, QueryDict

from unfriendly import settings
from unfriendly.utils import Obfuscator


def deobfuscate(request, key, juice=None):
    """
    Deobfuscates the URL and returns HttpResponse from source view.
    SEO juice is mostly ignored as it is intended for display purposes only.
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

    # fix-up the request object
    request.path = path
    request.path_info = path
    request.GET = QueryDict(query)
    request.META['QUERY_STRING'] = query
    request.META['PATH_INFO'] = path

    response = view(request, *args, **kwargs)

    # offer up a friendlier juice-powered filename if downloaded
    if juice and not response.has_header('Content-Disposition'):
        response['Content-Disposition'] = 'inline; filename=%s' % juice

    return response
