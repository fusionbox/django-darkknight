# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('darkknight', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatesigningrequest',
            name='created_at',
            field=models.DateTimeField(default=timezone.now(), auto_now_add=True),
            preserve_default=False,
        ),
    ]
