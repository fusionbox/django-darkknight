from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import EncryptedPrivateKey


class EncryptedPrivateKeyView(DetailView):
    queryset = EncryptedPrivateKey.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), key__uuid=self.kwargs['uuid']
        )

    def render_to_response(self, context):
        return HttpResponse(
            content=context['object'].encrypted_private_key,
            content_type='text/plain',
        )

gpg_key = EncryptedPrivateKeyView.as_view()
