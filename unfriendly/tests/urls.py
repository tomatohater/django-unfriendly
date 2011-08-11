from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns('unfriendly.tests.views',
    url(r'^test-view/$', 'test_view', name='unfriendly-test'),
)

urlpatterns += patterns('',
    url(r'^',   include('unfriendly.urls')),
)
