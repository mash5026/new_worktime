# Generated by Django 5.0.1 on 2025-01-21 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationaldocument',
            name='name_doc',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='نام مدرک تحصیلی'),
        ),
        migrations.AddField(
            model_name='trainingcertificate',
            name='name_doc',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='نام گواهینامه'),
        ),
    ]
