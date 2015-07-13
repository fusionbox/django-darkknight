import errno

from django.core.management.base import BaseCommand

from darkknight.models import SSLKey
from darkknight_gpg.apps import gpg_encrypt


class Command(BaseCommand):
    help = 'Imports all gpg keys in the key dir into the database, encrypting them.'

    def handle(self, *args, **options):
        for key in SSLKey.objects.filter(encryptedprivatekey=None):
            try:
                with open(key.key_path, 'r') as f:
                    gpg_encrypt(sender=self, instance=key, private_key=f.read())
            except IOError as e:
                if e.errno == errno.ENOENT:
                    pass
                else:
                    raise
