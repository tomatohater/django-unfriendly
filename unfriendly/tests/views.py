from django.http import HttpResponse


def test_view(request):
    return HttpResponse('this is a test')
