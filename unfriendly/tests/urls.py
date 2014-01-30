# -*- coding: utf-8 -*-
"""Url handlers for tests."""

try:
    from django.conf.urls import include, patterns, url
except ImportError:
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
