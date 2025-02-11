# Generated by Django 4.2.1 on 2024-08-11 23:44

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_bank_userbankaccount_bank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankaccount',
            name='bank',
            field=models.ForeignKey(blank=True, default=accounts.models.get_default_bank, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.bank'),
        ),
    ]
