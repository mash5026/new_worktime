from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from iranian_cities.fields import CityField
from persons.middleware import get_current_user
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

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
        ('سیکل', 'سیکل'),
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('کارشناسی', 'کارشناسی'),
        ('کارشناسی ارشد', 'کارشناسی ارشد'),
        ('دکترا', 'دکترا'),
        ('فوق دکترا', 'فوق دکترا'),
        ('مدارک حوزوی', 'مدارک حوزوی'),
    ]

    HOME_OWNERSHIP_CHOICES = [
        ('مالک', 'مالک'),
        ('مستاجر', 'مستاجر'),
        ('خانه پدری', 'خانه پدری'),
    ]

    NATIONALITY_CHOICES = [
        ('ایرانی', 'ایرانی'),
        ('غیر ایرانی', 'غیر ایرانی'),
    ]

    RELIGION_CHOICES = [
        ('اسلام', 'اسلام'),
        ('مسیحیت', 'مسیحیت'),
        ('زرتشت', 'زرتشت'),
        ('یهودیت', 'یهودیت'),
        ('سایر', 'سایر'),
    ]

    SECT_CHOICES = [
        ('سنی', 'سنی'),
        ('شیعه', 'شیعه'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('مجرد', 'مجرد'),
        ('متاهل', 'متاهل'),
        ('سایر', 'سایر'),
    ]

    MILITARY_SERVICE_CHOICES = [
        ('انجام شده', 'انجام شده'),
        ('انجام نشده', 'انجام نشده'),
        ('معافیت پزشکی', 'معافیت پزشکی'),
        ('معافیت غیرپزشکی', 'معافیت غیرپزشکی'),
        ('در حال انجام', 'در حال انجام'),
        ('سایر', 'سایر'),
    ]

    HAIR_COLOR_CHOICES = [
        ('قهوه ای', 'قهوه ای'),
        ('مشکی', 'مشکی'),
        ('سفید', 'سفید'),
        ('بلوند', 'بلوند'),
        ('سایر', 'سایر'),
    ]

    JOB_TITLE_CHOICES = [
        ('کارشناس', 'کارشناس'),
        ('کارشناس ارشد', 'کارشناس ارشد'),
        ('رئیس', 'رئیس'),
        ('معاون', 'معاون'),
        ('مدیر', 'مدیر'),
        ('مدیرعامل', 'مدیرعامل'),
        ('آبدارچی', 'آبدارچی'),
        ('نگهبان', 'نگهبان'),
        ('راننده', 'راننده'),
        ('مسئول دفتر', 'مسئول دفتر'),
        ('کارآموز', 'کارآموز'),
    ]

    ORGANIZATIONAL_UNIT_CHOICES = [
        ('مدیریت / معاونت سرمایه انسانی', 'مدیریت / معاونت سرمایه انسانی'),
        ('مدیریت / معاونت عملیات و پشتیبانی', 'مدیریت / معاونت عملیات و پشتیبانی'),
        ('مدیریت / معاونت فناوری اطلاعات', 'مدیریت / معاونت فناوری اطلاعات'),
        ('مدیریت / معاونت کسب و کار', 'مدیریت / معاونت کسب و کار'),
        ('مدیریت / معاونت برنامه ریزی', 'مدیریت / معاونت برنامه ریزی'),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        ('تمام وقت', 'تمام وقت'),
        ('پاره وقت', 'پاره وقت'),
        ('ساعتی', 'ساعتی'),
        ('مشاور', 'مشاور'),
        ('قطع همکاری', 'قطع همکاری'),
    ]


    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کارمند")
    NATIONALID = models.CharField(max_length=10, unique=True, verbose_name="کد ملی")
    identity_number = models.CharField(max_length=20, verbose_name="شماره شناسنامه")
    father_name = models.CharField(max_length=100, verbose_name="نام پدر")
    birth_places = CityField(null=True, blank=True, verbose_name="محل تولد", related_name='birth_places_personnel')
    birth_certificate_issue_city = CityField(null=True, blank=True, verbose_name='محل صدور شناسنامه', related_name='birth_certificate_issue_city_personnel')
    address = models.CharField(max_length=50, unique=True, verbose_name="محل سکونت")
    phone_number = models.CharField(max_length=50, unique=True, verbose_name="تلفن ثابت", null=True, blank=True)
    callphone = models.CharField(max_length=50, unique=True, verbose_name="شماره همراه")
    home_owner = models.CharField(
        max_length=20,
        choices=HOME_OWNERSHIP_CHOICES,
        default='owner',
        verbose_name='نوع تملک',
    )
    owner_file = models.FileField(
        upload_to='documents/owner/',
        verbose_name="تصویر یا فایل سند/اجاره نامه",
        validators=[validate_file_extension],
        null=True, blank=True
    )
    number_of_children = models.IntegerField(verbose_name='تعداد فرزند')
    education_level = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES,
        default='diploma', verbose_name="میزان تحصلات")
    Insurance_records = models.FloatField(verbose_name='مجموع سوابق بیمه (سال)')
    national_card_file_front = models.FileField(
        upload_to='documents/national_card/',
        verbose_name="روی تصویر یا فایل کارت ملی",
        validators=[validate_file_extension],
        null=True, blank=True
    )
    national_card_file_back = models.FileField(
        upload_to='documents/national_card/',
        verbose_name="پشت تصویر یا فایل کارت ملی",
        validators=[validate_file_extension],
        null=True, blank=True
    )
    birth_date = jmodels.jDateField(verbose_name="تاریخ تولد")
    insurance_number = models.CharField(max_length=20, verbose_name="شماره بیمه", null=True, blank=True)
    resume_file = models.FileField(
        upload_to='documents/resume/',
        verbose_name="فایل یا تصویر رزومه",
        validators=[validate_file_extension],
        null=True, blank=True
    )
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
    military_service_front = models.FileField(
        upload_to='documents/military_service/',
        verbose_name="روی تصویر یا فایل کارت پایان خدمت",
        validators=[validate_file_extension],
        null=True, blank=True
    )

    military_service_back = models.FileField(
        upload_to='documents/military_service/',
        verbose_name="پشت تصویر یا فایل کارت پایان خدمت",
        validators=[validate_file_extension],
        null=True, blank=True
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
    account_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='شماره حساب بانک رفاه کارگران')
    sheba_number = models.CharField(max_length=60, blank=True, null=True, verbose_name='شماره شبای بانک رفاه کارگران')
    card_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='شماره کارت بانک رفاه کارگران')
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
        ('سیکل', 'سیکل'),
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('کارشناسی', 'کارشناسی'),
        ('کارشناسی ارشد', 'کارشناسی ارشد'),
        ('دکترا', 'دکترا'),
        ('فوق دکترا', 'فوق دکترا'),
        ('مدارک حوزوی', 'مدارک حوزوی'),
    ]
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='educational_documents', verbose_name="پرسنل")
    name_doc = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES,
        default='diploma', verbose_name='نام مدرک تحصیلی', null=True, blank=True)
    document_file = models.FileField(
        upload_to='documents/educational/',
        verbose_name="فایل یا تصویر مدرک تحصیلی",
        validators=[validate_file_extension],
        null=True, blank=True
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
        validators=[validate_file_extension],
        null=True, blank=True
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
        validators=[validate_file_extension],
        null=True, blank=True
    )

    class Meta:
        verbose_name = "سابقه بیمه"
        verbose_name_plural = "سوابق بیمه"


class EmploymentHistory(models.Model):
    
    JOB_TITLE_CHOICES = [
        ('کارشناس', 'کارشناس'),
        ('کارشناس ارشد', 'کارشناس ارشد'),
        ('رئیس', 'رئیس'),
        ('معاون', 'معاون'),
        ('مدیر', 'مدیر'),
        ('مدیرعامل', 'مدیرعامل'),
        ('آبدارچی', 'آبدارچی'),
        ('نگهبان', 'نگهبان'),
        ('راننده', 'راننده'),
        ('مسئول دفتر', 'مسئول دفتر'),
        ('کارآموز', 'کارآموز'),
    ]

    ORGANIZATIONAL_UNIT_CHOICES = [
        ('مدیریت / معاونت سرمایه انسانی', 'مدیریت / معاونت سرمایه انسانی'),
        ('مدیریت / معاونت عملیات و پشتیبانی', 'مدیریت / معاونت عملیات و پشتیبانی'),
        ('مدیریت / معاونت فناوری اطلاعات', 'مدیریت / معاونت فناوری اطلاعات'),
        ('مدیریت / معاونت کسب و کار', 'مدیریت / معاونت کسب و کار'),
        ('مدیریت / معاونت برنامه ریزی', 'مدیریت / معاونت برنامه ریزی'),
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
        choices=JOB_TITLE_CHOICES,
        verbose_name="عنوان شغلی"
    )
    work_experience = models.FloatField(verbose_name="میزان سابقه (سال)")
    organizational_unit = models.CharField(
        max_length=50,
        choices=ORGANIZATIONAL_UNIT_CHOICES,
        verbose_name="واحد سازمانی"
    )

    class Meta:
        verbose_name = "سوابق شغلی"
        verbose_name_plural = "سوابق شغلی"

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"
    

class TypeDocRecords(TimeStampedModel):

    doc_title_choices = [
        ('firstpage', 'صفحه اول'),
        ('secondpage', 'صفحه دوم'),
        ('thirdpage', 'صفحه سوم'),
        ('fourthpage', 'صفحه چهارم'),
        ('fifthpage', 'صفحه پنجم')
    ]

    type_title_choices = [
        ('identitycardfile', 'شناسنامه'),
        ('passport', 'گذرنامه')
    ]

    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='typedocs_records', verbose_name="پرسنل")
    name_type = models.CharField(max_length=100, choices=type_title_choices, verbose_name='نوع مدرک', null=True, blank=True)
    name_doc = models.CharField(max_length=100, choices=doc_title_choices, verbose_name='نام صفحه', null=True, blank=True)
    serial_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='شماره سریال', help_text='د18/909090')
    
    certificate_file = models.FileField(
        upload_to='documents/typedoc/',
        verbose_name="فایل یا تصویر  مدرک",
        validators=[validate_file_extension],
        null=True, blank=True
    )

    class Meta:
        verbose_name = "مدرک شناسنامه/پاسپورت"
        verbose_name_plural = "مدارک شناسنامه/پاسپورت"


class License(models.Model):
    activation_date = models.DateTimeField(verbose_name="تاریخ فعال‌سازی", default=timezone.now)
    expiration_date = models.DateTimeField(verbose_name="تاریخ انقضا", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            self.expiration_date = self.activation_date + timedelta(days=90)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.expiration_date < timezone.now()
    

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="نام برند")

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"

    def __str__(self):
        return self.name
    
class NameAsset(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="نام کالا")

    class Meta:
        verbose_name = "نام کالا"
        verbose_name_plural = "نام کالاها"

    def __str__(self):
        return self.name
    

class Asset(models.Model):
    name = models.ForeignKey(NameAsset, on_delete=models.CASCADE, verbose_name="نام کالا")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="برند کالا")
    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="قیمت (ریال)")  
    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالاها"

    def __str__(self):
        return f"{self.name} - {self.brand}"
    

class AssetTransaction(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_assets", verbose_name="شخص تحویل گیرنده")
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_assets", verbose_name="شخص تحویل‌دهنده")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name="نام کالا", related_name="transactions")
    accesories = models.ForeignKey(NameAsset, on_delete=models.CASCADE, verbose_name="لوازم جانبی", null=True, blank=True)
    serial_number = models.CharField(max_length=255, unique=True, verbose_name="شماره پلاک", null=True, blank=True)
    receive_date = jmodels.jDateField(verbose_name="تاریخ دریافت", null=True, blank=True)
    return_date = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ تحویل")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    

    class Meta:
        verbose_name = "معامله دارایی"
        verbose_name_plural = "معاملات دارایی"

    def __str__(self):
        return f"{self.asset} | {self.serial_number} | {self.receiver}"
    
class AssetTransactionHistory(models.Model):
    asset_transaction = models.ForeignKey(AssetTransaction, on_delete=models.CASCADE, related_name="history", verbose_name="تراکنش اصلی")
    receiver = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="received_assets_history", verbose_name="شخص تحویل گیرنده")
    giver = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="given_assets_history", verbose_name="شخص تحویل‌دهنده")
    receive_date = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ دریافت")
    return_date = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ تحویل")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "تاریخچه معامله دارایی"
        verbose_name_plural = "تاریخچه معاملات دارایی"

    def __str__(self):
        return f"{self.asset_transaction.asset} | {self.receive_date} | {self.receiver}"

    def save(self, *args, **kwargs):
        # به‌روز رسانی تاریخ تحویل در AssetTransaction
        if self.receive_date and not self.asset_transaction.return_date:
            self.asset_transaction.return_date = self.receive_date
            self.asset_transaction.save()
        super().save(*args, **kwargs)