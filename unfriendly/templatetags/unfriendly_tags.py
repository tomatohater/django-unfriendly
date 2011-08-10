from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from unfriendly import settings
from unfriendly.utils import Obfuscator


register = template.Library()


@register.filter
def obfuscate(value, juice=None):
    """
    Template filter that obfuscates whatever text it is applied to. The text is
    supposed to be a URL, but it will obfuscate any text.

    Usage:
        Extremely unfriendly URL:
        {{ "/my-site-path/"|obfuscate }}

        Include some SEO juice:
        {{ "/my-site-path/"|obfuscate:"some SEO friendly text" }}
    """
    obfuscator = Obfuscator(settings.UNFRIENDLY_SECRET)

    kwargs = {
        'key': obfuscator.obfuscate(*[value]),
    }

    if juice:
        kwargs['juice'] = slugify(juice)

    return reverse('unfriendly-deobfuscate', kwargs=kwargs)
