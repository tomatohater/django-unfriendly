django-unfriendly
========================

django-unfriendly is a Django app that obfuscates urls and allows your application to natively execute the original url's view.

There is lots of talk about SEO friendly urls. The trend is towards more and more readable human information in your urls and Django makes it easy to create urls like::

    http://yoursite.com/music/black-sabbath-is-awesome/

But sometimes urls can give too much away. This is where django-unfriendly comes in.

django-unfriendly provides a template filter that obfuscates urls in your templates, and a url handler that deobfuscates and executes the original view (no redirection).


Why?
****

Perhaps you have a Django application with urls like the one above and you don't want anyone tampering with your urls or guessing other possibilities::

    http://yoursite.com/music/melvins-are-awesome/

You can obfuscation the url which might look like::

    http://yoursite.com/u/E5v4uxuNSA8I2is33c6V8lqFTcdv_IxPLDGG/

Tampering with the obfuscated url should return a ``404 - Page not found`` error.

Obfuscated urls are idempotent and may be safely cached.


Installation
************

1. Install the ``django-unfriendly`` package::

    # with pip
    pip install django-unfriendly

    # or with easy_install
    easy_install django-unfriendly

2. Make sure you have any ``pycrypto`` installed::

    # with pip
    pip install pycrypto

    # or with easy_install
    easy_install pycrypto

3. Add ``unfriendly`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'unfriendly',
        ...
    )

4. Add ``unfriendly.urls`` to your ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^u/', include('unfriendly.urls')),
        ...
    )




Usage
******
Load this tag library into any templates where you want to use django-unfriendly::

    {% load unfriendly_tags %}

Then apply the obfuscate filter to any url you'd like to hide::

    <a href="{{ "/music/black-sabbath-is-awesome/"|obfuscate }}">Sabbath awesome</a>

Or with ``{% url view %}`` reversal::

    {% url path.to.view as melvins_url %}
    <a href="{{ melvins_url|obfuscate }}">Melvins awesome</a>

If SEO is still important to you, you can pass some SEO juice to the filter::

    <a href="{{ melvins_url|obfuscate:"King Buzzo rocks" }}">Melvins awesome</a>


Setting
******

The following may be added to your setting.py to customize the behavior of this app.

 - ``UNFRIENDLY_SECRET``

   - default: ``SECRET_KEY``
   - Used for encryption/decryption. Note: AES keys must be either 16, 24, or 32 bytes long.

 - ``UNFRIENDLY_ENFORCE_CHECKSUM``

   - default: ``True``
   - Determines whether or not the decrypted data is validatedagainst a crc checksum to detect tampering.


Credits
********
* `Drew Engelson`_
* Inspiration from `django-urlcrypt`_
* Python encryption with crc from `Alon Swartz`_

.. _`Drew Engelson`: http://github.com/tomatohater
.. _`django-urlcrypt`: http://github.com/dziegler/django-urlcrypt
.. _`Alon Swartz`: http://www.turnkeylinux.org/blog/python-symmetric-encryption
