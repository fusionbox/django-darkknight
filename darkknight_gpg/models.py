from django.db import models
from django.core import urlresolvers


class EncryptedPrivateKey(models.Model):
    key = models.OneToOneField('darkknight.SSLKey')
    encrypted_private_key = models.TextField()

    def get_absolute_url(self):
        return urlresolvers.reverse('darkknight_gpg.views.gpg_key', kwargs={'uuid': self.key.uuid})
