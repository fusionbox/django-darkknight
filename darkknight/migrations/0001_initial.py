# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateSigningRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=255)),
                ('key', models.FilePathField(verbose_name=b'/home/rocky/projects/fusionbox/csr.fusionbox.com/csr/../tmp/keys', match=b'*.key')),
                ('csr', models.FilePathField(verbose_name=b'/home/rocky/projects/fusionbox/csr.fusionbox.com/csr/../tmp/keys', match=b'*.csr')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
