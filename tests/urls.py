# -*- coding: utf-8 -*-
"""Url handlers for tests."""

from django.conf.urls import include, url

from .views import test_view


urlpatterns = [
    url(r'^test-view/$', test_view, name='unfriendly-test'),
    url(r'^' + 'test-view' * 20 + '/$', test_view, name='unfriendly-test-long'),
    url(r'^', include('unfriendly.urls')),
]
