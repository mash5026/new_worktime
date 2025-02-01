# Generated by Django 5.0.1 on 2025-01-25 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0006_personnel_education_level_personnel_home_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='father_name',
            field=models.CharField(default=0, max_length=100, verbose_name='نام پدر'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personnel',
            name='hair_color',
            field=models.CharField(choices=[('brown', 'قهوه ای'), ('black', 'مشکی'), ('white', 'سفید'), ('blonde', 'بلوند'), ('other', 'سایر')], default='brown', max_length=20, verbose_name='رنگ مو'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='height',
            field=models.FloatField(default=0, verbose_name='قد'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personnel',
            name='job_title',
            field=models.CharField(choices=[('expert', 'کارشناس'), ('senior_expert', 'کارشناس ارشد'), ('chief', 'رئیس'), ('deputy', 'معاون'), ('manager', 'مدیر'), ('ceo', 'مدیرعامل'), ('janitor', 'آبدارچی'), ('guard', 'نگهبان'), ('driver', 'راننده'), ('office_manager', 'مسئول دفتر'), ('intern', 'کارآموز')], default='expert', max_length=20, verbose_name='عنوان شغلی'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='marital_status',
            field=models.CharField(choices=[('single', 'مجرد'), ('married', 'متاهل'), ('other', 'سایر')], default='single', max_length=20, verbose_name='وضعیت تاهل'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='military_service',
            field=models.CharField(choices=[('done', 'انجام شده'), ('not_done', 'انجام نشده'), ('medical_exemption', 'معافیت پزشکی'), ('non_medical_exemption', 'معافیت غیرپزشکی'), ('in_progress', 'در حال انجام'), ('other', 'سایر')], default='done', max_length=40, verbose_name='وضعیت خدمت سربازی'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='nationality',
            field=models.CharField(choices=[('iranian', 'ایرانی'), ('foreign', 'غیر ایرانی')], default='iranian', max_length=20, verbose_name='ملیت'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='organizational_title',
            field=models.CharField(choices=[('expert', 'کارشناس'), ('senior_expert', 'کارشناس ارشد'), ('chief', 'رئیس'), ('deputy', 'معاون'), ('manager', 'مدیر'), ('ceo', 'مدیرعامل'), ('janitor', 'آبدارچی'), ('guard', 'نگهبان'), ('driver', 'راننده'), ('office_manager', 'مسئول دفتر'), ('intern', 'کارآموز')], default='expert', max_length=50, verbose_name='عنوان سازمانی'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='organizational_unit',
            field=models.CharField(choices=[('human_resources_management', 'مدیریت / معاونت سرمایه انسانی'), ('operations_support_management', 'مدیریت / معاونت عملیات و پشتیبانی'), ('it_management', 'مدیریت / معاونت فناوری اطلاعات'), ('business_management', 'مدیریت / معاونت کسب و کار'), ('planning_management', 'مدیریت / معاونت برنامه ریزی')], default='human_resources_management', max_length=50, verbose_name='واحد سازمانی'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='religion',
            field=models.CharField(choices=[('islam', 'اسلام'), ('christianity', 'مسیحیت'), ('zoroastrianism', 'زرتشت'), ('judaism', 'یهودیت'), ('other', 'سایر')], default='islam', max_length=20, verbose_name='دین'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='sect',
            field=models.CharField(choices=[('sunni', 'سنتی'), ('shia', 'شیعه')], default='shia', max_length=20, verbose_name='مذهب'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='weight',
            field=models.FloatField(default=0, verbose_name='وزن'),
            preserve_default=False,
        ),
    ]
