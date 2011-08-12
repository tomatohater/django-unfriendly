from urllib import unquote
from urlparse import urlparse

from django.core.urlresolvers import resolve, Resolver404
from django.http import HttpResponseNotFound, QueryDict

from unfriendly import settings
from unfriendly.utils import decrypt, CheckSumError


def deobfuscate(request, key, juice=None):
    """
    Deobfuscates the URL and returns HttpResponse from source view.
    SEO juice is mostly ignored as it is intended for display purposes only.
    """
    try:
        url = decrypt(str(key),
                      settings.UNFRIENDLY_SECRET,
                      checksum=settings.UNFRIENDLY_ENFORCE_CHECKSUM)
    except CheckSumError:
        return HttpResponseNotFound()

    url_parts = urlparse(unquote(url))
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
