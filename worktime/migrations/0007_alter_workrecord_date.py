# Generated by Django 5.0.2 on 2024-02-13 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktime', '0006_alter_workrecord_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workrecord',
            name='date',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
