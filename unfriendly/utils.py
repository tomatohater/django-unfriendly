import base64
import zlib
import struct
from Crypto.Cipher import AES


class CheckSumError(Exception):
    pass


def _lazysecret(secret, blocksize=32, padding='}'):
    """Pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding
    return secret


def encrypt(plaintext, secret, iv, checksum=True, lazy=True):
    """Encrypts plaintext with secret
    plaintext   - content to encrypt
    secret      - secret to encrypt plaintext
    lazy        - pad secret if less than legal blocksize (default: True)
    checksum    - attach crc32 byte encoded (default: True)
    returns ciphertext
    """

    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB, iv)

    if checksum:
        plaintext += base64.urlsafe_b64encode(
            struct.pack("i", zlib.crc32(plaintext)))

    return base64.urlsafe_b64encode(encobj.encrypt(plaintext)).replace('=', '')


def decrypt(ciphertext, secret, iv, checksum=True, lazy=True):
    """Decrypts ciphertext with secret
    ciphertext  - encrypted content to decrypt
    secret      - secret to decrypt ciphertext
    lazy        - pad secret if less than legal blocksize (default: True)
    checksum    - verify crc32 byte encoded checksum (default: True)
    returns plaintext
    """

    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB, iv)
    plaintext = encobj.decrypt(base64.urlsafe_b64decode(
        ciphertext + ('=' * (len(ciphertext) % 4))))

    if checksum:
        try:
            crc, plaintext = (base64.urlsafe_b64decode(
                plaintext[-8:]), plaintext[:-8])
        except TypeError:
            raise CheckSumError("checksum mismatch")

        if not crc == struct.pack("i", zlib.crc32(plaintext)):
            raise CheckSumError("checksum mismatch")

    return plaintext
