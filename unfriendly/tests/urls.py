# -*- coding: utf-8 -*-
"""Url handlers for tests."""

import django

if django.VERSION >= (1, 9):

    from django.conf.urls import include, url
    from unfriendly.tests.views import test_view

    urlpatterns = [
        url(r'^test-view/$', test_view, name='unfriendly-test'),
        url(r'^', include('unfriendly.urls'))
    ]

else:

    if django.VERSION >= (1, 4):
        from django.conf.urls import include, patterns, url
    else:
        # For Django versions older than 1.4 (removed in 1.6)
        from django.conf.urls.defaults import include, patterns, url


    urlpatterns = patterns(
        'unfriendly.tests.views',
        url(r'^test-view/$', 'test_view', name='unfriendly-test'),
    )

    urlpatterns += patterns(
        '',
        url(r'^', include('unfriendly.urls')),
    )
