# -*- coding: utf-8 -*-
"""Url handlers."""

import django
from distutils.version import StrictVersion

DJANGO_VERSION = StrictVersion(django.get_version)

if DJANGO_VERSION >= StrictVersion('1.9'):

    from django.conf.urls import url
    from unfriendly.views import deobfuscate

    urlpatterns = [
        # Mostly unfriendly URL (but with SEO juice).
        url(r'^(?P<juice>.+)/(?P<key>.+)/$', deobfuscate,
            name='unfriendly-deobfuscate'),

        # Extremely unfriendly URL (no SEO juice).
        url(r'^(?P<key>.+)/$', deobfuscate, name='unfriendly-deobfuscate')
    ]

else:

    if DJANGO_VERSION >= StrictVersion('1.5'):
        from django.conf.urls import patterns, url
    else:
        from django.conf.urls.defaults import patterns, url

    urlpatterns = patterns(
        'unfriendly.views',

        # Mostly unfriendly URL (but with SEO juice).
        url(r'^(?P<juice>.+)/(?P<key>.+)/$', 'deobfuscate',
            name='unfriendly-deobfuscate'),

        # Extremely unfriendly URL (no SEO juice).
        url(r'^(?P<key>.+)/$', 'deobfuscate', name='unfriendly-deobfuscate'),
    )

