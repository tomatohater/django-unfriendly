# -*- coding: utf-8 -*-
"""Various encryption utilites."""

import base64
import struct
import zlib

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


def encrypt(plaintext, secret, inital_vector, checksum=True, lazy=True):
    """Encrypts plaintext with secret
    plaintext      - content to encrypt
    secret         - secret to encrypt plaintext
    inital_vector  - initial vector
    lazy           - pad secret if less than legal blocksize (default: True)
    checksum       - attach crc32 byte encoded (default: True)
    returns ciphertext
    """

    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB, inital_vector)

    if checksum:
        plaintext += base64.urlsafe_b64encode(
            struct.pack("i", zlib.crc32(plaintext)))

    return base64.urlsafe_b64encode(encobj.encrypt(plaintext)).replace('=', '')


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
        plaintext = encobj.decrypt(base64.urlsafe_b64decode(
            ciphertext + ('=' * (len(ciphertext) % 4))))
    except TypeError:
        raise InvalidKeyError("invalid key")

    if checksum:
        try:
            crc, plaintext = (base64.urlsafe_b64decode(
                plaintext[-8:]), plaintext[:-8])
        except TypeError:
            raise CheckSumError("checksum mismatch")

        if not crc == struct.pack("i", zlib.crc32(plaintext)):
            raise CheckSumError("checksum mismatch")

    return plaintext
