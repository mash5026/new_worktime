# Generated by Django 5.0.1 on 2025-01-25 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0015_alter_personnel_insurance_records'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='Insurance_records',
            field=models.FloatField(verbose_name='مجموع سوابق بیمه (سال)'),
        ),
    ]
