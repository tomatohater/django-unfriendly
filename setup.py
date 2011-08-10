from setuptools import setup, find_packages
import unfriendly
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name = "django-unfriendly",
    version = unfriendly.__version__,
    description = 'The unfriendliest urls in town.',
    long_description = README,
    url = 'http://github.com/tomatohater/django-unfriendly',
    author = 'Drew Engelson',
    author_email = 'drew@engelson.net',
    license = 'BSD',
    zip_safe = False,
    packages = find_packages(),
    include_package_data = True,
    package_data = {},
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
