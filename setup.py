# -*- coding: utf-8 -*-
"""Setup file for django-unfriendly."""

import os

import unfriendly
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name = "django-unfriendly",
    version = unfriendly.__version__,
    description = 'The unfriendliest urls in town! Django app that obfuscates urls and allows your application to natively execute the original view.',
    long_description = README,
    url = 'http://github.com/tomatohater/django-unfriendly',
    author = 'Drew Engelson',
    author_email = 'drew@engelson.net',
    license='MIT',
    zip_safe = False,
    packages = find_packages(),
    include_package_data = True,
    package_data = {},
    install_requires = [
        'pycrypto>=2.0.1',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
