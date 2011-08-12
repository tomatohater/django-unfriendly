import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from unfriendly import settings
from unfriendly.utils import encrypt, decrypt
from unfriendly.templatetags.unfriendly_tags import obfuscate


class UnfriendlyTests(TestCase):
    urls = 'unfriendly.tests.urls'

    def setUp(self):
        self.juice = 'Lorem ipsum dolor sit amet'

    def test_encryption(self):
        """
        Test the encryption.
        """
        original = self.juice

        obfuscated = encrypt(original, settings.UNFRIENDLY_SECRET)
        self.assertNotEqual(original, obfuscated)

        deobfuscated = decrypt(obfuscated, settings.UNFRIENDLY_SECRET)
        self.assertEqual(original, deobfuscated)

    def test_obfuscate_filter(self):
        """
        Test the obfuscate filter.
        """
        test_url = reverse('unfriendly-test')
        obfuscated_url = obfuscate(test_url)
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'key': encrypt(test_url, settings.UNFRIENDLY_SECRET),
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
            'key': encrypt(test_url, settings.UNFRIENDLY_SECRET),
        })
        self.assertEqual(view_url, obfuscated_url)

    def test_deobfuscate_view(self):
        """
        Test the deobfuscate view.
        """
        test_url = reverse('unfriendly-test')
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

    def test_deobfuscate_view_404(self):
        """
        Test deobfuscate view with hacked url.
        """
        view_url = reverse('unfriendly-deobfuscate', kwargs={
            'key': 'hacked-key',
        })
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 404)
