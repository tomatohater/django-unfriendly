# -*- coding: utf-8 -*-
"""Default settings for package (overridable with Django settings)."""

from django.conf import settings

#
# UNFRIENDLY_SECRET is used for encryption/decryption
# Note: AES keys must be either 16, 24, or 32 bytes long
#
UNFRIENDLY_SECRET = getattr(settings, 'UNFRIENDLY_SECRET',
                            getattr(settings, 'SECRET_KEY')[0:32])
if not UNFRIENDLY_SECRET:
    UNFRIENDLY_SECRET = 'hush' * 8

#
# UNFRIENDLY_IV is the initial vector required by AES cipher
# Note: AES initial vector must be 16 bytes long
#
UNFRIENDLY_IV = getattr(settings, 'UNFRIENDLY_IV',
                        getattr(settings, 'SECRET_KEY')[0:16])
if not UNFRIENDLY_IV:
    UNFRIENDLY_IV = 'hush' * 4

#
# UNFRIENDLY_ENFORCE_CHECKSUM whether or not the decrypted data is validated
# against a crc checksum to detect tampering
#
UNFRIENDLY_ENFORCE_CHECKSUM = getattr(settings,
                                      'UNFRIENDLY_ENFORCE_CHECKSUM', True)
