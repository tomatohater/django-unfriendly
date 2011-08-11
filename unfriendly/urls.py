from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('unfriendly.views',
    # Mostly unfriendly URL (but with SEO juice).
    url(r'^(?P<juice>.+)/(?P<key>.+)/$', 'deobfuscate',
        name='unfriendly-deobfuscate'),

    # Extremely unfriendly URL (no SEO juice).
    url(r'^(?P<key>.+)/$', 'deobfuscate', name='unfriendly-deobfuscate'),
)
