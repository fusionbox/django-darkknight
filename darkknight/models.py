from django.db import models
from django.core.signing import Signer
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

pk_signer = Signer('CSR PK')


@python_2_unicode_compatible
class CertificateSigningRequest(models.Model):
    domain = models.CharField(max_length=255)
    key = models.FilePathField(settings.DARKKNIGHT_STORAGE, match="*.key")
    csr = models.FilePathField(settings.DARKKNIGHT_STORAGE, match="*.csr")

    def __str__(self):
        return 'Certificate for %s' % self.domain

    @property
    def signed_pk(self):
        return pk_signer.sign(self.pk)
