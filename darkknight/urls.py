from django.conf.urls import patterns, url

urlpatterns = patterns('darkknight.views',
    url(r'^$', 'generate'),
    url(r'^detail/(?P<signed_pk>[^/]+)/$', 'redirect_to_detail'),
    url(r'^download/(?P<signed_pk>[^/]+)/$', 'redirect_to_download'),
    url(r'^csr/(?P<uuid>[^/]+)/$', 'detail'),
    url(r'^csr/(?P<uuid>[^/]+)/view/$', 'download'),
)
