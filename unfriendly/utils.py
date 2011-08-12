import base64
import zlib
import struct
from Crypto.Cipher import AES

class CheckSumError(Exception):
    pass

def _lazysecret(secret, blocksize=32, padding='}'):
    """pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding
    return secret

def encrypt(plaintext, secret, lazy=True, checksum=True):
    """encrypt plaintext with secret
    plaintext   - content to encrypt
    secret      - secret to encrypt plaintext
    lazy        - pad secret if less than legal blocksize (default: True)
    checksum    - attach crc32 byte encoded (default: True)
    returns ciphertext
    """

    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)

    if checksum:
        plaintext += struct.pack("i", zlib.crc32(plaintext))

    return base64.urlsafe_b64encode(encobj.encrypt(plaintext)).replace('=', '')

def decrypt(ciphertext, secret, lazy=True, checksum=True):
    """decrypt ciphertext with secret
    ciphertext  - encrypted content to decrypt
    secret      - secret to decrypt ciphertext
    lazy        - pad secret if less than legal blocksize (default: True)
    checksum    - verify crc32 byte encoded checksum (default: True)
    returns plaintext
    """

    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)
    plaintext = encobj.decrypt(base64.urlsafe_b64decode(
        ciphertext + ('=' * (len(ciphertext) % 4))))

    if checksum:
        crc, plaintext = (plaintext[-4:], plaintext[:-4])
        if not crc == struct.pack("i", zlib.crc32(plaintext)):
            raise CheckSumError("checksum mismatch")

    return plaintext
