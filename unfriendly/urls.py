# -*- coding: utf-8 -*-
"""Url handlers."""

import django


if django.VERSION >= (1, 9):

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

    if django.VERSION >= (1, 4):
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

