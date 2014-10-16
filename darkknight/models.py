import os.path
import uuid

from django.db import models
from django.core.signing import Signer
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from OpenSSL import crypto

pk_signer = Signer('CSR PK')


@python_2_unicode_compatible
class CertificateSigningRequest(models.Model):
    # for search over the domain
    domain = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=32, unique=True, default=lambda: uuid.uuid4().hex)

    def __str__(self):
        return 'Certificate for %s' % self.domain

    @property
    def key_path(self):
        return os.path.join(settings.DARKKNIGHT_STORAGE, '%s.key' % self.uuid)

    @property
    def csr_path(self):
        return os.path.join(settings.DARKKNIGHT_STORAGE, '%s.csr' % self.uuid)

    def get_csr_text(self):
        with open(self.csr_path, 'r') as f:
            return f.read()

    def get_csr_obj(self):
        return crypto.load_certificate_request(crypto.FILETYPE_PEM, self.get_csr_text())
