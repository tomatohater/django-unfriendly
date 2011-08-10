import base64

from django.utils.hashcompat import sha_constructor
from django.conf import settings


class Obfuscator(object):
    """
    Handles string obfuscation and deobfuscation.

    Usage:
    >>> o = Obfuscator('secret-key')
    >>> o.obfuscate('cleartext')
    'vJqxni-3Mrcx'
    >>> o.deobfuscate('vJqxni-3Mrcx')
    'cleartext'
    """
    obfuscation_key = None

    def __init__(self, secret):
        self.obfuscation_key = (sha_constructor(secret).digest() +
                                sha_constructor(secret[::-1]).digest())


    def xor_map_string(self, data):
        """
        Returns obfuscated string (also deobfuscates).
        """
        key = self.obfuscation_key * (len(data)//len(self.obfuscation_key) + 1)
        xor_gen = (chr(ord(t) ^ ord(k)) for t, k in zip(data, key))
        return ''.join(xor_gen)


    def obfuscate(self, data):
        """
        Obfuscates string in url-safe fashion.
        """
        return base64.urlsafe_b64encode(
            self.xor_map_string(data)).replace('=', '')


    def deobfuscate(self, data):
        """
        Deobfuscates string.
        """
        return self.xor_map_string(
            base64.urlsafe_b64decode(data + ('=' * (len(data) % 4))))
