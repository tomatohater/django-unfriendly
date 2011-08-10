from django.conf import settings

"""
UNFRIENDLY_SECRET is used for obfuscation and encryption.
"""
UNFRIENDLY_SECRET = getattr(settings, 'UNFRIENDLY_SECRET',
                            getattr(settings, 'SECRET_KEY', 'hush-hush'))
