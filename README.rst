django-unfriendly
=================

The unfriendliest urls in town! ``django-unfriendly`` is a Django app that obfuscates urls and allows your application to natively execute the original view.

.. image:: https://travis-ci.org/tomatohater/django-unfriendly.png?branch=master
    :target: https://travis-ci.org/tomatohater/django-unfriendly

.. image:: https://coveralls.io/repos/tomatohater/django-unfriendly/badge.png?branch=master
	:target: https://coveralls.io/r/tomatohater/django-unfriendly?branch=master

.. image:: https://badge.fury.io/py/django-unfriendly.png
    :target: http://badge.fury.io/py/django-unfriendly

There is lots of talk about SEO friendly urls. The trend is towards more and more human readable information in your urls and Django makes it easy to create urls like::

    http://yoursite.com/music/awesome/the-melvins/

But sometimes urls can give too much away. This is where ``django-unfriendly`` comes in.

``django-unfriendly`` provides a template filter that obfuscates urls in your templates, and a url handler/view that deobfuscates and executes the original view (e.g. no redirection).


Read the docs
*************

https://django-unfriendly.readthedocs.org/en/latest/

Version compatibility
*********************

- v0.5.0
    - Python 2.7
    - Django 1.8, 1.9, 1.10
- v0.4.1
    - Python 2.6 and 2.7
    - Django 1.0 - 1.8

Python 3+ support coming soon...
