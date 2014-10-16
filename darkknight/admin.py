from django.contrib import admin
from django.http import Http404
from django.shortcuts import redirect

from darkknight.models import CertificateSigningRequest


class CertificateSigningRequestAdmin(admin.ModelAdmin):
    list_display = ['created_at', '__unicode__', 'domain']
    list_display_links = ['__unicode__', 'domain']
    list_filter = ['domain', 'created_at']
    search_fields = ['domain']

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, from_url='', extra_context=None):
        try:
            obj = CertificateSigningRequest.objects.get(pk=object_id)
        except CertificateSigningRequest.DoesNotExist:
            raise Http404

        return redirect('darkknight.views.detail', uuid=obj.uuid)

admin.site.register(CertificateSigningRequest, CertificateSigningRequestAdmin)
