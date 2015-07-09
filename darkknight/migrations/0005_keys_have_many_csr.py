# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import errno

from django.db import models, migrations
from django.conf import settings
import darkknight.models

def csr_path(csr):
    """
    Copy pasted from darkknight/models.py#CertificateSigningRequest.csr_path
    """
    return os.path.join(settings.DARKKNIGHT_STORAGE, '%s.csr' % csr.uuid)


def csr_from_disk_to_database(state, schema_editor):
    CSR = state.get_model('darkknight', 'certificatesigningrequest')
    for csr in CSR.objects.all():
        path = csr_path(csr)
        with open(path, 'r') as fp:
            csr.content = fp.read()
        csr.save()


def create_associated_keys(state, schema_editor):
    Key = state.get_model('darkknight', 'sslkey')
    CSR = state.get_model('darkknight', 'certificatesigningrequest')
    for csr in CSR.objects.all():
        Key.objects.create(uuid=csr.key_id)


class Migration(migrations.Migration):

    dependencies = [
        ('darkknight', '0004_auto_20150708_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSLKey',
            fields=[
                ('uuid', models.CharField(default=darkknight.models.generate_uuid, max_length=32, unique=True, serialize=False, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='certificatesigningrequest',
            name='content',
            field=models.TextField(default='a'),
            preserve_default=False,
        ),
        migrations.RunPython(csr_from_disk_to_database),
        migrations.RenameField(
            model_name='certificatesigningrequest',
            old_name='uuid',
            new_name='key',
        ),
        migrations.AlterField(
            model_name='certificatesigningrequest',
            name='key',
            field=models.ForeignKey(to='darkknight.SSLKey'),
            preserve_default=True,
        ),
        # This is a one way function because keys can have CSR, and uuid are unique on CSR
        migrations.RunPython(create_associated_keys),
    ]
