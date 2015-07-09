import os.path
import uuid

from django.db import models
from django.core.signing import Signer
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from OpenSSL import crypto

pk_signer = Signer('CSR PK')


# must be a top-level function to be serializable in migrations
def generate_uuid():
    return uuid.uuid4().hex


class SSLKey(models.Model):
    uuid = models.CharField(max_length=32, unique=True, default=generate_uuid, primary_key=True)

    @property
    def key_path(self):
        return os.path.join(settings.DARKKNIGHT_STORAGE, '%s.key' % self.uuid)


@python_2_unicode_compatible
class CertificateSigningRequest(models.Model):
    # for search over the domain
    domain = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    key = models.ForeignKey(SSLKey, related_name='csr_set')

    def __str__(self):
        return 'Certificate for %s' % self.domain

    @property
    def csr_path(self):
        return os.path.join(settings.DARKKNIGHT_STORAGE, '%s.csr' % self.uuid)

    @property
    def csr_obj(self):
        return crypto.load_certificate_request(crypto.FILETYPE_PEM, self.content)

    @property
    def subject(self):
        return self.csr_obj.get_subject()
