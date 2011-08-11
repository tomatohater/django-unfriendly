from django.http import HttpResponse


def test_view(request):
    return HttpResponse(request.get_full_path())
