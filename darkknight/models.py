from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Key(models.Model):
    key = models.FilePathField(settings.DARKKNIGHT_STORAGE, match="*.key")
    csr = models.FilePathField(settings.DARKKNIGHT_STORAGE, match="*.csr")
    # This is a cached for speed. This can be pulled from the csr file
    _csr_commonname = models.CharField(max_length=255)

    def __str__(self):
        return 'CSR for %s' % self._csr_commonname

