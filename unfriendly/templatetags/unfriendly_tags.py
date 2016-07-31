# -*- coding: utf-8 -*-
"""Module contains package templatetags."""

from django import template
from django.template.defaultfilters import slugify
from unfriendly import settings
from unfriendly.utils import encrypt

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


register = template.Library()


@register.filter
def obfuscate(value, juice=None):
    """
    Template filter that obfuscates whatever text it is applied to. The text is
    supposed to be a URL, but it will obfuscate anything.

    Usage:
        Extremely unfriendly URL:
        {{ "/my-secret-path/"|obfuscate }}

        Include some SEO juice:
        {{ "/my-secret-path/"|obfuscate:"some SEO friendly text" }}
    """
    if not settings.UNFRIENDLY_ENABLE_FILTER:
        return value
    kwargs = {
        'key': encrypt(value,
                       settings.UNFRIENDLY_SECRET,
                       settings.UNFRIENDLY_IV,
                       checksum=settings.UNFRIENDLY_ENFORCE_CHECKSUM),
    }
    if juice:
        kwargs['juice'] = slugify(juice)
    return reverse('unfriendly-deobfuscate', kwargs=kwargs)
