# -*- coding: utf-8 -*-
"""Url handlers."""

from django.conf.urls import url

from unfriendly import views

urlpatterns = [
    # Mostly unfriendly URL (but with SEO juice).
    url(r'^(?P<juice>.+)/(?P<key>.+)/$', views.deobfuscate,
        name='unfriendly-deobfuscate'),

    # Extremely unfriendly URL (no SEO juice).
    url(r'^(?P<key>.+)/$', views.deobfuscate, name='unfriendly-deobfuscate'),
]
