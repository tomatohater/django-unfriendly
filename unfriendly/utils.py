# -*- coding: utf-8 -*-
"""Various encryption utilites."""

import base64
import binascii
import struct
import zlib

import six

from Crypto.Cipher import AES


class InvalidKeyError(Exception):
    """Invalid key error class."""
    pass

class CheckSumError(Exception):
    """Checksum mismatch error class."""
    pass


def _lazysecret(secret, blocksize=32, padding='}'):
    """Pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding
    return secret

def _crc(plaintext):
    """Generates crc32. Modulo keep the value within int range."""
    if not isinstance(plaintext, six.binary_type):
        plaintext = six.b(plaintext)
    return (zlib.crc32(plaintext) % 2147483647) & 0xffffffff

def _pack_crc(plaintext):
    """Packs plaintext crc32 as binary data."""
    return struct.pack('i', _crc(plaintext))

def encrypt(plaintext, secret, inital_vector, checksum=True, lazy=True):
    """Encrypts plaintext with secret
    plaintext      - content to encrypt
    secret         - secret to encrypt plaintext
    inital_vector  - initial vector
    lazy           - pad secret if less than legal blocksize (default: True)
    checksum       - attach crc32 byte encoded (default: True)
    returns ciphertext
    """
    if not isinstance(plaintext, six.binary_type):
        plaintext = six.b(plaintext)

    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB, inital_vector)

    if checksum:
        packed = _pack_crc(plaintext)
        plaintext += base64.urlsafe_b64encode(packed)

    encoded = base64.urlsafe_b64encode(encobj.encrypt(plaintext))
    if isinstance(plaintext, six.binary_type):
        encoded = encoded.decode()

    return encoded.replace('=', '')


def decrypt(ciphertext, secret, inital_vector, checksum=True, lazy=True):
    """Decrypts ciphertext with secret
    ciphertext     - encrypted content to decrypt
    secret         - secret to decrypt ciphertext
    inital_vector  - initial vector
    lazy           - pad secret if less than legal blocksize (default: True)
    checksum       - verify crc32 byte encoded checksum (default: True)
    returns plaintext
    """
    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB, inital_vector)
    try:
        padded = ciphertext + ('=' * (len(ciphertext) % 4))
        decoded = base64.urlsafe_b64decode(str(padded))
        plaintext = encobj.decrypt(decoded)
    except (TypeError, binascii.Error):
        raise InvalidKeyError("invalid key")

    if checksum:
        try:
            crc, plaintext = (base64.urlsafe_b64decode(
                plaintext[-8:]), plaintext[:-8])
        except (TypeError, binascii.Error):
            raise CheckSumError("checksum mismatch")

        if not crc == _pack_crc(plaintext):
            raise CheckSumError("checksum mismatch")

    return plaintext
