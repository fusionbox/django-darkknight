from django.core.signing import BadSignature
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

from darkknight.forms import GenerateForm
from darkknight.models import CertificateSigningRequest, pk_signer


class GenerateView(FormView):
    template_name = 'darkknight/generate.html'
    form_class = GenerateForm

    def get_success_url(self):
        assert hasattr(self, 'instance')
        return reverse(
            detail,
            kwargs=dict(uuid=self.instance.uuid),
        )

    def form_valid(self, form):
        self.instance = form.generate()
        return super(GenerateView, self).form_valid(form)


class CertificateSigningRequestMixin(SingleObjectMixin):
    model = CertificateSigningRequest
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class DetailView(CertificateSigningRequestMixin, DetailView):
    template_name = 'darkknight/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['csr'] = context['object'].get_csr_obj().get_subject()
        return context


class DownloadView(CertificateSigningRequestMixin, SingleObjectMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        csr = self.object.get_csr_text()

        response = HttpResponse(csr, content_type='text/plain')

        if 'download' in request.GET:
            content_disposition = 'attachement; filename="{}"'.format(
                '%s.csr' % slugify(self.object.domain))
            response['Content-Disposition'] = content_disposition
        elif 'view' not in request.GET:
            raise Http404

        return response


generate = GenerateView.as_view()
detail = DetailView.as_view()
download = DownloadView.as_view()


# Before putting the csr uuid in the url, we used a signed pk. These views
# redirect the old urls to the new ones.
def get_csr_from_signed_pk(signed_pk):
    try:
        pk = pk_signer.unsign(signed_pk)
    except BadSignature:
        raise Http404

    return get_object_or_404(CertificateSigningRequest, pk=pk)


def redirect_to_detail(request, signed_pk):
    obj = get_csr_from_signed_pk(signed_pk)
    return HttpResponseRedirect(reverse(detail, kwargs={'uuid': obj.uuid}))


def redirect_to_download(request, signed_pk):
    obj = get_csr_from_signed_pk(signed_pk)
    return HttpResponseRedirect(reverse(download, kwargs={'uuid': obj.uuid}))
