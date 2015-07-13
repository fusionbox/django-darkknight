import shutil
import tempfile
from contextlib import contextmanager

import gnupg

from django.apps import AppConfig
from django.conf import settings

from darkknight.signals import key_created
from .models import EncryptedPrivateKey


class DarkKnightGpgConfig(AppConfig):
    name = 'darkknight_gpg'

    def ready(self):
        key_created.connect(gpg_encrypt)


@contextmanager
def tmp_gpg_context():
    try:
        tmpdir = tempfile.mkdtemp()
        yield gnupg.GPG(homedir=tmpdir)
    finally:
        shutil.rmtree(tmpdir)


def gpg_encrypt(sender, instance, private_key, **kwargs):
    with open(settings.GPG_PUBLIC_KEY_PATH) as f:
        public_key = f.read()

    with tmp_gpg_context() as gpg:
        import_result = gpg.import_keys(public_key)
        assert import_result.counts['count'] >= 1, import_result.stderr
        encryption_result = gpg.encrypt(private_key, *import_result.fingerprints)
        assert encryption_result.ok, encryption_result.stderr

    EncryptedPrivateKey.objects.create(
        key=instance,
        encrypted_private_key=str(encryption_result),
    )
