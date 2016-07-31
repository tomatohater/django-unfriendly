# -*- coding: utf-8 -*-
"""Django view handlers for tests."""

from django.http import HttpResponse


def test_view(request):
    """"Test view."""
    return HttpResponse(request.get_full_path())
