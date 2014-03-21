# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateSigningRequest',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=255)),
                ('key', models.FilePathField(verbose_name='/tmp', match='*.key')),
                ('csr', models.FilePathField(verbose_name='/tmp', match='*.csr')),
                ('crt', models.FilePathField(default=None, null=True, verbose_name='/tmp', match='*.crt')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
