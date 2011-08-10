django-unfriendly
========================

django-unfriendly is a Django app that obfuscates URLs and allows your application to handle with your native Django views.

There is lots of talk about SEO friendly URLs. The trend is towards more and more readable information in your URLs. Django makes it easy to create URLs like::

    http://yoursite.com/music/black-sabbath-is-awesome/

But sometimes these URLs can give too much away. This is where django-unfriendly comes in.

django-unfriendly provides a template filter that obfuscates URLs in your templates, and then provides a URL handler that deobfuscates and executes the original view.

Why?
****

Perhaps you have a Django application with URLs like the one above. And you don't want anyone tampering with your URLs by guessing other possibilities like this::::

    http://yoursite.com/music/melvins-are-awesome/

You can apply the obfuscation filter to in your template tag which might result in a URL like this::

    http://yoursite.com/u/E5v4uxuNSA8I2is33c6V8lqFTcdv_IxPLDGG/


Installation
************

1. ``easy_install django-unfriendly`` or ``pip install django-unfriendly``

2. Add ``unfriendly`` to your ``INSTALLED_APPS``

3. Add ``unfriendly.urls`` to your ``urls.py``::

    urlpatterns = patterns('',
        url(r'^u/', include('unfriendly.urls')),
    )


Usage
******
Load this tag library into any templates where you want to use django-unfriendly::

    {% load unfriendly_tags %}

Then apply the obfuscate filter to any URL you'd like to hide::

    <a href="{{ "/music/black-sabbath-is-awesome/"|obfuscate }}">Sabbath awesome</a>

Or with the ``url`` reversal::

    {% url path.to.view as melvins_url %}
    <a href="{{ melvins_url|obfuscate }}">Melvins awesome</a>

If SEO is still important to you, you can pass some SEO juice to the filter::

    <a href="{{ melvins_url|obfuscate:"King Buzzo rocks" }}">Melvins awesome</a>


Credits
********
`Drew Engelson`_

.. _`Drew Engelson`: http://github.com/tomatohater
