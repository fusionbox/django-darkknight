from django.core.signing import BadSignature
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponse
from django.utils.text import slugify

from OpenSSL import crypto
from darkknight.forms import GenerateForm
from darkknight.models import CertificateSigningRequest, pk_signer


class GenerateView(FormView):
    template_name = 'darkknight/generate.html'
    form_class = GenerateForm

    def get_success_url(self):
        assert hasattr(self, 'instance')
        return reverse(
            detail,
            kwargs=dict(signed_pk=self.instance.signed_pk),
        )

    def form_valid(self, form):
        self.instance = form.generate()
        return super(GenerateView, self).form_valid(form)


class CertificateSingingRequestMixin(object):
    model = CertificateSigningRequest

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object

        assert 'signed_pk' in self.kwargs
        if queryset is None:
            queryset = self.get_queryset()
        try:
            pk = pk_signer.unsign(self.kwargs['signed_pk'])
        except BadSignature:
            raise Http404

        try:
            self.object = queryset.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

        return self.object


class DetailView(CertificateSingingRequestMixin, DetailView):
    template_name = 'darkknight/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        assert 'signed_pk' in self.kwargs
        context['signed_pk'] = self.kwargs['signed_pk']

        obj = context['object']
        with open(obj.csr, 'r') as f:
            csr = f.read()

        req = crypto.load_certificate_request(crypto.FILETYPE_PEM, csr)
        context['csr'] = req.get_subject()

        return context



class DownloadView(CertificateSingingRequestMixin, SingleObjectMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        with open(self.object.csr, 'r') as f:
            csr = f.read()

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
