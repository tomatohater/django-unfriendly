# -*- coding: utf-8 -*-
"""Test suite for django-unfriendly."""

import datetime

import six

from django.http import HttpResponseNotFound
from django.template.defaultfilters import slugify
from django.test import TestCase
from mock import patch

from unfriendly import settings
from unfriendly.utils import CheckSumError, encrypt, decrypt
from unfriendly.templatetags.unfriendly_tags import obfuscate

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class UnfriendlyTests(TestCase):
    """Test case for django-unfriendly."""
    urls = 'tests.urls'

    def setUp(self):
        self.juice = six.b('Lorem ipsum dolor sit amet')

    def test_encryption(self):
        """
        Test the encryption.
        """
        original = self.juice

        obfuscated = encrypt(original, settings.UNFRIENDLY_SECRET,
                             settings.UNFRIENDLY_IV)
        self.assertNotEqual(original, obfuscated)

        deobfuscated = decrypt(obfuscated, settings.UNFRIENDLY_SECRET,
                               settings.UNFRIENDLY_IV)
        self.assertEqual(original, deobfuscated)

    def test_encryption_oddkey(self):
        """
        Test the encryption with an odd length secret key.
        """
        original = self.juice

        obfuscated = encrypt(original, settings.UNFRIENDLY_SECRET[0:11],
                             settings.UNFRIENDLY_IV)
        self.assertNotEqual(original, obfuscated)

        deobfuscated = decrypt(obfuscated, settings.UNFRIENDLY_SECRET[0:11],
                               settings.UNFRIENDLY_IV)
        self.assertEqual(original, deobfuscated)

    def test_encryption_checksum(self):
        """
        Test the encryption with bad checksums.
        """
        original = self.juice

        obfuscated = encrypt(original, settings.UNFRIENDLY_SECRET,
                             settings.UNFRIENDLY_IV)

        # Add characters to the end (cannot unpack checksum)
        self.assertRaises(
            CheckSumError,
            decrypt, obfuscated + 'oops', settings.UNFRIENDLY_SECRET,
            settings.UNFRIENDLY_IV)

        # Replace last few characters (checksum mismatch)
        self.assertRaises(
            CheckSumError,
            decrypt, obfuscated[-4:] + 'oops', settings.UNFRIENDLY_SECRET,
            settings.UNFRIENDLY_IV)

    def test_obfuscate_filter(self):
        """
        Test the obfuscate filter.
        """
        test_url = reverse('unfriendly-test')
        obfuscated_url = obfuscate(test_url)
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'key': encrypt(test_url, settings.UNFRIENDLY_SECRET,
                           settings.UNFRIENDLY_IV),
        })
        self.assertEqual(view_url, obfuscated_url)

    def test_obfuscate_long_filter(self):
        """
        Test the obfuscate filter.
        """
        test_url = reverse('unfriendly-test-long')
        obfuscated_url = obfuscate(test_url)
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'key': encrypt(test_url, settings.UNFRIENDLY_SECRET,
                           settings.UNFRIENDLY_IV),
        })
        self.assertEqual(view_url, obfuscated_url)

    def test_obfuscate_filter_with_juice(self):
        """
        Test the obfuscate filter.
        """
        test_url = reverse('unfriendly-test')
        obfuscated_url = obfuscate(test_url, self.juice)
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'juice': slugify(self.juice),
            'key': encrypt(test_url, settings.UNFRIENDLY_SECRET,
                           settings.UNFRIENDLY_IV),
        })
        self.assertEqual(view_url, obfuscated_url)

    @patch('unfriendly.templatetags.unfriendly_tags.settings.UNFRIENDLY_ENABLE_FILTER',
           False)
    def test_obfuscate_filter_disabled(self):
        """
        Test the obfuscate filter when disabled in settings.
        """
        test_url = reverse('unfriendly-test')
        obfuscated_url = obfuscate(test_url)
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'key': encrypt(test_url, settings.UNFRIENDLY_SECRET,
                           settings.UNFRIENDLY_IV),
        })
        self.assertNotEqual(view_url, obfuscated_url)
        self.assertNotEqual(view_url, test_url)

    @patch('unfriendly.templatetags.unfriendly_tags.settings.UNFRIENDLY_ENABLE_FILTER',
           False)
    def test_obfuscate_filter_with_juice_disabled(self):
        """
        Test the obfuscate filter when disabled in settings.
        """
        test_url = reverse('unfriendly-test')
        obfuscated_url = obfuscate(test_url, self.juice)
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'juice': slugify(self.juice),
            'key': encrypt(test_url, settings.UNFRIENDLY_SECRET,
                           settings.UNFRIENDLY_IV),
        })
        self.assertNotEqual(view_url, obfuscated_url)
        self.assertNotEqual(view_url, test_url)

    def test_deobfuscate_view(self):
        """
        Test the deobfuscate view.
        """
        test_url = reverse('unfriendly-test')
        obfuscated_url = obfuscate(test_url)

        test_response = self.client.get(test_url)
        obfuscated_response = self.client.get(obfuscated_url)

        self.assertEqual(test_response.content, obfuscated_response.content)

    def test_deobfuscate_long_view(self):
        """
        Test the deobfuscate view.
        """
        test_url = reverse('unfriendly-test-long')
        obfuscated_url = obfuscate(test_url)

        test_response = self.client.get(test_url)
        obfuscated_response = self.client.get(obfuscated_url)

        self.assertEqual(test_response.content, obfuscated_response.content)

    def test_deobfuscate_view_with_juice(self):
        """
        Test the deobfuscate view with seo juice.
        """
        test_url = reverse('unfriendly-test')
        obfuscated_url = obfuscate(test_url, self.juice)

        test_response = self.client.get(test_url)
        obfuscated_response = self.client.get(obfuscated_url)

        self.assertEqual(test_response.content, obfuscated_response.content)

    def test_deobfuscate_view_bad_path(self):
        """
        Test the deobfuscate view with a bad url path.
        """
        test_url = 'bad-path'
        obfuscated_url = obfuscate(test_url)
        response = self.client.get(obfuscated_url)
        self.assertEqual(response.status_code, 404)

    def test_deobfuscate_view_404(self):
        """
        Test deobfuscate view with hacked url.
        """
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'key': 'hacked-key',
        })
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 404)

    def test_deobfuscate_view_404_invalid_key(self):
        """
        Test deobfuscate view with an invalid key (too short).
        """
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'key': 'i',
        })
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 404)
