# Generated by Django 5.0.1 on 2025-02-03 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0029_rename_name_asset_nameasset'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nameasset',
            options={'verbose_name': 'نام کالا', 'verbose_name_plural': 'نام کالاها'},
        ),
        migrations.AlterField(
            model_name='assettransaction',
            name='accesories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accessory_transactions', to='persons.asset', verbose_name='لوازم جانبی'),
        ),
        migrations.AlterField(
            model_name='assettransaction',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='persons.asset', verbose_name='نام کالا'),
        ),
    ]
