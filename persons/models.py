from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from iranian_cities.fields import CityField
from persons.middleware import get_current_user
from django.contrib.auth import get_user_model

User = get_user_model()


def user_str(self):
    return f"{self.first_name} {self.last_name} ({self.username})"

User.add_to_class("__str__", user_str)


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]  # استخراج پسوند فایل
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']  # پسوندهای مجاز
    if ext.lower() not in valid_extensions:
        raise ValidationError('فقط فایل‌های JPG, JPEG, PNG و PDF مجاز هستند.')
    

class TimeStampedModel(models.Model):
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_%(class)s", verbose_name="ثبت‌کننده")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_%(class)s", verbose_name="بروزرسانی‌کننده")

    class Meta:
        abstract = True

    @property
    def first_name(self):
        return self.person.first_name if self.person else ""

    @property
    def last_name(self):
        return self.person.last_name if self.person else ""

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk and not self.created_by:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)



class Personnel(TimeStampedModel):
    EDUCATION_LEVEL_CHOICES = [
        ('cycle', 'سیکل'),
        ('diploma', 'دیپلم'),
        ('associate', 'فوق دیپلم'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('doctorate', 'دکترا'),
        ('postdoctorate', 'فوق دکترا'),
        ('seminary', 'مدارک حوزوی'),
    ]

    HOME_OWNERSHIP_CHOICES = [
        ('owner', 'مالک'),
        ('renter', 'مستاجر'),
        ('family_home', 'خانه پدری'),
    ]

    NATIONALITY_CHOICES = [
        ('iranian', 'ایرانی'),
        ('foreign', 'غیر ایرانی'),
    ]

    RELIGION_CHOICES = [
        ('islam', 'اسلام'),
        ('christianity', 'مسیحیت'),
        ('zoroastrianism', 'زرتشت'),
        ('judaism', 'یهودیت'),
        ('other', 'سایر'),
    ]

    SECT_CHOICES = [
        ('sunni', 'سنتی'),
        ('shia', 'شیعه'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'مجرد'),
        ('married', 'متاهل'),
        ('other', 'سایر'),
    ]

    MILITARY_SERVICE_CHOICES = [
        ('done', 'انجام شده'),
        ('not_done', 'انجام نشده'),
        ('medical_exemption', 'معافیت پزشکی'),
        ('non_medical_exemption', 'معافیت غیرپزشکی'),
        ('in_progress', 'در حال انجام'),
        ('other', 'سایر'),
    ]

    HAIR_COLOR_CHOICES = [
        ('brown', 'قهوه ای'),
        ('black', 'مشکی'),
        ('white', 'سفید'),
        ('blonde', 'بلوند'),
        ('other', 'سایر'),
    ]

    JOB_TITLE_CHOICES = [
        ('expert', 'کارشناس'),
        ('senior_expert', 'کارشناس ارشد'),
        ('chief', 'رئیس'),
        ('deputy', 'معاون'),
        ('manager', 'مدیر'),
        ('ceo', 'مدیرعامل'),
        ('janitor', 'آبدارچی'),
        ('guard', 'نگهبان'),
        ('driver', 'راننده'),
        ('office_manager', 'مسئول دفتر'),
        ('intern', 'کارآموز'),
    ]

    ORGANIZATIONAL_UNIT_CHOICES = [
        ('human_resources_management', 'مدیریت / معاونت سرمایه انسانی'),
        ('operations_support_management', 'مدیریت / معاونت عملیات و پشتیبانی'),
        ('it_management', 'مدیریت / معاونت فناوری اطلاعات'),
        ('business_management', 'مدیریت / معاونت کسب و کار'),
        ('planning_management', 'مدیریت / معاونت برنامه ریزی'),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        ('full_time', 'تمام وقت'),
        ('part_time', 'پاره وقت'),
        ('hourly', 'ساعتی'),
        ('consultant', 'مشاور'),
        ('terminated', 'قطع همکاری'),
    ]


    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کارمند")
    national_id = models.CharField(max_length=10, unique=True, verbose_name="کد ملی")
    identity_number = models.CharField(max_length=20, verbose_name="شماره شناسنامه")
    father_name = models.CharField(max_length=100, verbose_name="نام پدر")
    birth_places = CityField(null=True, blank=True, verbose_name="محل تولد", related_name='birth_places_personnel')
    birth_certificate_issue_city = CityField(null=True, blank=True, verbose_name='محل صدور شناسنامه', related_name='birth_certificate_issue_city_personnel')
    address = models.CharField(max_length=50, unique=True, verbose_name="آدرس")
    phone_number = models.CharField(max_length=50, unique=True, verbose_name="تلفن ثابت")
    callphone = models.CharField(max_length=50, unique=True, verbose_name="تلفن همراه")
    home_owner = models.CharField(
        max_length=20,
        choices=HOME_OWNERSHIP_CHOICES,
        default='owner',
        verbose_name='نوع تملک',
    )
    number_of_children = models.IntegerField(verbose_name='تعداد فرزند')
    education_level = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES,
        default='diploma', verbose_name="میزان تحصیلی")
    Insurance_records = models.FloatField(verbose_name='مجموع سوابق بیمه (سال)')
    national_card_file = models.FileField(
        upload_to='documents/national_card/',
        verbose_name="تصویر یا فایل کارت ملی",
        validators=[validate_file_extension]
    )
    birth_date = jmodels.jDateField(verbose_name="تاریخ تولد")
    identity_card_file = models.FileField(
        upload_to='documents/identity_card/',
        verbose_name="تصویر یا فایل شناسنامه",
        validators=[validate_file_extension]
    )
    insurance_number = models.CharField(max_length=20, verbose_name="شماره بیمه")
    profile_image = models.ImageField(
            upload_to='documents/profile_images/',
            verbose_name="عکس پرسنلی",
            null=True,
            blank=True
        )
    job_title = models.CharField(
            max_length=20,
            choices=JOB_TITLE_CHOICES,
            default='expert',
            verbose_name="عنوان شغلی"
        )
    nationality = models.CharField(
            max_length=20,
            choices=NATIONALITY_CHOICES,
            default='iranian',
            verbose_name="ملیت"
        )
    religion = models.CharField(
            max_length=20,
            choices=RELIGION_CHOICES,
            default='islam',
            verbose_name="دین"
        )
    sect = models.CharField(
            max_length=20,
            choices=SECT_CHOICES,
            default='shia',
            verbose_name="مذهب"
        )
    marital_status = models.CharField(
            max_length=20,
            choices=MARITAL_STATUS_CHOICES,
            default='single',
            verbose_name="وضعیت تاهل"
        )
    weight = models.FloatField(verbose_name="وزن")
    height = models.FloatField(verbose_name="قد")
    military_service = models.CharField(
            max_length=40,
            choices=MILITARY_SERVICE_CHOICES,
            default='done',
            verbose_name="وضعیت خدمت سربازی"
        )
    hair_color = models.CharField(
            max_length=20,
            choices=HAIR_COLOR_CHOICES,
            default='brown',
            verbose_name="رنگ مو"
        )
    organizational_title = models.CharField(
            max_length=50,
            choices=JOB_TITLE_CHOICES,
            default='expert',
            verbose_name="عنوان سازمانی"
        )
    organizational_unit = models.CharField(
            max_length=50,
            choices=ORGANIZATIONAL_UNIT_CHOICES,
            default='human_resources_management',
            verbose_name="واحد سازمانی"
        )
    
    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default='full_time',
        verbose_name="وضعیت کارمند"
    )

    class Meta:
        verbose_name = "پرسنل"
        verbose_name_plural = "پرسنل‌ها"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_date(self):
        return self.birth_date.strftime('%Y/%m/%d')
    get_date.short_description="تاریخ تولد"


class EducationalDocument(TimeStampedModel):

    EDUCATION_LEVEL_CHOICES = [
        ('cycle', 'سیکل'),
        ('diploma', 'دیپلم'),
        ('associate', 'فوق دیپلم'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('doctorate', 'دکترا'),
        ('postdoctorate', 'فوق دکترا'),
        ('seminary', 'مدارک حوزوی'),
    ]
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='educational_documents', verbose_name="پرسنل")
    name_doc = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES,
        default='diploma', verbose_name='نام مدرک تحصیلی', null=True, blank=True)
    document_file = models.FileField(
        upload_to='documents/educational/',
        verbose_name="فایل یا تصویر مدرک تحصیلی",
        validators=[validate_file_extension]
    )

    class Meta:
        verbose_name = "مدرک تحصیلی"
        verbose_name_plural = "مدارک تحصیلی"


class TrainingCertificate(TimeStampedModel):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='training_certificates', verbose_name="پرسنل")
    name_doc = models.CharField(max_length=100, verbose_name='نام گواهینامه', null=True, blank=True)
    certificate_file = models.FileField(
        upload_to='documents/training/',
        verbose_name="فایل یا تصویر گواهینامه آموزشی",
        validators=[validate_file_extension]
    )

    class Meta:
        verbose_name = "گواهینامه آموزشی"
        verbose_name_plural = "گواهینامه‌های آموزشی"


class InsuranceRecords(TimeStampedModel):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='insurance_records', verbose_name="پرسنل")
    name_doc = models.CharField(max_length=100, verbose_name='نوع سابقه بیمه', null=True, blank=True)
    certificate_file = models.FileField(
        upload_to='documents/training/',
        verbose_name="فایل یا تصویر  سابقه",
        validators=[validate_file_extension]
    )

    class Meta:
        verbose_name = "سابقه بیمه"
        verbose_name_plural = "سوابق بیمه"


class EmploymentHistory(models.Model):
    
    job_title_choices = [
        ('expert', 'کارشناس'),
        ('senior_expert', 'کارشناس ارشد'),
        ('chief', 'رئیس'),
        ('deputy', 'معاون'),
        ('manager', 'مدیر'),
        ('ceo', 'مدیرعامل'),
        ('janitor', 'آبدارچی'),
        ('guard', 'نگهبان'),
        ('driver', 'راننده'),
        ('office_manager', 'مسئول دفتر'),
        ('intern', 'کارآموز'),
    ]
    
    organizational_unit_choices = [
        ('human_resources_management', 'مدیریت / معاونت سرمایه انسانی'),
        ('operations_support_management', 'مدیریت / معاونت عملیات و پشتیبانی'),
        ('it_management', 'مدیریت / معاونت فناوری اطلاعات'),
        ('business_management', 'مدیریت / معاونت کسب و کار'),
        ('planning_management', 'مدیریت / معاونت برنامه ریزی'),
    ]

    personnel = models.ForeignKey(
        Personnel,
        related_name='employment_histories',
        on_delete=models.CASCADE,
        verbose_name="پرسنل"
    )
    company_name = models.CharField(max_length=255, verbose_name="نام شرکت")
    job_title = models.CharField(
        max_length=50,
        choices=job_title_choices,
        verbose_name="عنوان شغلی"
    )
    work_experience = models.FloatField(verbose_name="میزان سابقه (سال)")
    organizational_unit = models.CharField(
        max_length=50,
        choices=organizational_unit_choices,
        verbose_name="واحد سازمانی"
    )

    class Meta:
        verbose_name = "سوابق شغلی"
        verbose_name_plural = "سوابق شغلی"

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"
