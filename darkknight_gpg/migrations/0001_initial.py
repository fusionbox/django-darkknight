# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('darkknight', '0005_keys_have_many_csr'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptedPrivateKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('encrypted_private_key', models.TextField()),
                ('key', models.OneToOneField(to='darkknight.SSLKey')),
            ],
        ),
    ]
