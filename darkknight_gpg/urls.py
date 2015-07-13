from django.conf.urls import url


urlpatterns = [
    url(r'^csr/(?P<uuid>[^/]+)/gpg-key/$', 'darkknight_gpg.views.gpg_key'),
]
