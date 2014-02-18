from django.conf.urls import patterns, url

urlpatterns = patterns('darkknight.views',
    url(r'^$', 'generate'),
    url(r'^detail/(?P<signed_pk>[^/]+)/$', 'detail'),
    url(r'^download/(?P<signed_pk>[^/]+)/$', 'download'),
)
