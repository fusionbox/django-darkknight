# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path

from django.db import models, migrations
from django.conf import settings


def path_to_uuid(state, schema_editor):
    CSR = state.get_model('darkknight', 'certificatesigningrequest')
    for csr in CSR.objects.all():
        csr.uuid = os.path.splitext(os.path.basename(csr.csr))[0]
        csr.save()


def uuid_to_path(state, schema_editor):
    CSR = state.get_model('darkknight', 'certificatesigningrequest')
    for csr in CSR.objects.all():
        csr.key = os.path.join(settings.DARKKNIGHT_STORAGE, csr.uuid) + '.key'
        csr.csr = os.path.join(settings.DARKKNIGHT_STORAGE, csr.uuid) + '.csr'
        csr.save()


class Migration(migrations.Migration):

    dependencies = [
        ('darkknight', '0002_certificatesigningrequest_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatesigningrequest',
            name='uuid',
            field=models.CharField(default=None, null=True, unique=True, max_length=32),
            preserve_default=False,
        ),

        migrations.AlterField(
            model_name='certificatesigningrequest',
            name='key',
            field=models.FilePathField(settings.DARKKNIGHT_STORAGE, match="*.key", null=True),
        ),
        migrations.AlterField(
            model_name='certificatesigningrequest',
            name='csr',
            field=models.FilePathField(settings.DARKKNIGHT_STORAGE, match="*.csr", null=True),
        ),

        migrations.RunPython(path_to_uuid, uuid_to_path),

        migrations.RemoveField(
            model_name='certificatesigningrequest',
            name='csr',
        ),
        migrations.RemoveField(
            model_name='certificatesigningrequest',
            name='key',
        ),
    ]
