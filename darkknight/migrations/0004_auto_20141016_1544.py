# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import darkknight.models


class Migration(migrations.Migration):

    dependencies = [
        ('darkknight', '0003_auto_20141015_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatesigningrequest',
            name='uuid',
            field=models.CharField(default=darkknight.models.generate_uuid4, help_text='', unique=True, max_length=32),
        ),
    ]
