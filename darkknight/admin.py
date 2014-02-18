from django.contrib import admin
from django.http import Http404
from django.shortcuts import redirect

from darkknight.models import CertificateSigningRequest

class CertificateSigningRequestAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, from_url='', extra_context=None):
        try:
            obj = CertificateSigningRequest.objects.get(pk=object_id)
        except CertificateSigningRequest.DoesNotExist:
            raise Http404

        return redirect('darkknight.views.detail', signed_pk=obj.signed_pk)

admin.site.register(CertificateSigningRequest, CertificateSigningRequestAdmin)
