from django.core.signing import BadSignature
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.forms.formsets import formset_factory

from darkknight.forms import GenerateBaseFormSet, GenerateForm
from darkknight.models import CertificateSigningRequest, pk_signer, SSLKey


class GenerateView(FormView):
    template_name = 'darkknight/generate.html'

    def get_form_class(self):
        try:
            n = int(self.request.GET['n'])
        except (ValueError, KeyError):
            n = 1

        return formset_factory(
            GenerateForm,
            formset=GenerateBaseFormSet,
            extra=n,
            max_num=50,
        )

    def get_success_url(self):
        assert hasattr(self, 'instance')
        return reverse(
            detail,
            kwargs=dict(uuid=self.instance.uuid),
        )

    def form_valid(self, form):
        self.instance = form.generate()
        return super(GenerateView, self).form_valid(form)


class DetailView(DetailView):
    template_name = 'darkknight/detail.html'
    queryset = SSLKey.objects.prefetch_related('csr_set')
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class DownloadView(SingleObjectMixin, View):
    http_method_names = ['get']
    model = CertificateSigningRequest

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            key__uuid=self.kwargs['uuid'],
            pk=self.kwargs['pk'],
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        response = HttpResponse(self.object.content, content_type='text/plain')

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

    qs = CertificateSigningRequest.objects.all().select_related('key')
    return get_object_or_404(qs, pk=pk)


def redirect_to_detail(request, signed_pk):
    obj = get_csr_from_signed_pk(signed_pk)
    return HttpResponseRedirect(reverse(detail, kwargs={'uuid': obj.key.uuid}))


def redirect_to_download(request, signed_pk):
    obj = get_csr_from_signed_pk(signed_pk)
    return HttpResponseRedirect(reverse(download, kwargs={'uuid': obj.key.uuid, 'pk': obj.pk}))

def redirect_to_default_download(request, uuid):
    try:
        obj = CertificateSigningRequest.objects.get(key__uuid=uuid)
        url = reverse(download, kwargs={'uuid': obj.key.uuid, 'pk': obj.pk})
        if request.GET:
            url += '?' + request.GET.urlencode()
        return HttpResponseRedirect(url)
    except CertificateSigningRequest.MultipleObjectsReturned:
        raise Http404("This key has many certificates")
