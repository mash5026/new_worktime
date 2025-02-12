from collections.abc import Iterable
from django.db import models
from .utils import LIST_ANSWER, PRESENT, ABSENT
from datetime import datetime, time
from django_jalali.db import models as jmodels
from jalali_date import datetime2jalali, date2jalali
import jdatetime
from django.contrib.auth.models import User
from persons.middleware import get_current_user
from django.core.exceptions import ValidationError

def user_str(self):
    return f"{self.first_name} {self.last_name} ({self.username})"

User.add_to_class("__str__", user_str)

# Assuming LIST_ANSWER and status choices are defined elsewhere as mentioned
ABSENT = 'A'
PRESENT = 'P'
DOFF = 'DO'
HOFF = 'HO'
MISSION = 'M'
SICKNESS = 'S'

LIST_ANSWER = [(ABSENT, 'غایب'), (PRESENT, 'حاضر'), (DOFF, 'مرخصی روزانه'), (HOFF, 'مرخصی ساعتی'),(MISSION, 'ماموریت'), (SICKNESS, 'استعلاجی')]

class WorkRecord(models.Model):
    person = models.CharField(max_length=100)
    date = models.DateField()  # Changed from CharField to DateField for proper date handling
    arrived_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    night_work = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_morning = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    normal_working_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_evening = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    work_nights = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    work_deduction_morning = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    work_deduction_evening = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=LIST_ANSWER, default=PRESENT)

    def save(self, *args, **kwargs):
        self._calculate_status()
        super().save(*args, **kwargs)

    def _calculate_status(self):
        """Calculate the employee's presence status based on arrival and departure times."""
        # Example logic - adjust according to actual business rules
        if self.arrived_time is not None and self.departure_time is not None:
            arrived_dt = datetime.combine(self.date, self.arrived_time)
            departure_dt = datetime.combine(self.date, self.departure_time)
            total_hours = (departure_dt - arrived_dt).total_seconds() / 3600

            # Set status to absent if arriving after 12 noon or working less than the required hours
            noon_time = time(12, 0)
            if self.arrived_time > noon_time or total_hours < 5:
                self.status = ABSENT
            else:
                self.status = PRESENT
        else:
            # Consider absent if there's no arrival or departure time
            self.status = ABSENT

    class Meta:
        ordering = ['date', 'person']
        verbose_name = 'Work Record'
        verbose_name_plural = 'Work Records'

    def __str__(self):
        return f"{self.person} on {self.date}"
    

class Holiday(models.Model):
    date_holiday = models.DateField()
    event = models.CharField(max_length=200)


class WorkRecordFinally(models.Model):
    person = models.CharField(max_length=100)
    date = models.DateField(null=True)
    date_persian = jmodels.jDateField(blank=True, null=True)
    weekday_name = models.CharField(max_length=15, blank=True, null=True)
    normal_working_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    normal_working_hours_formatted = models.CharField(max_length=10, blank=True, null=True)
    over_time = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    over_time_formatted = models.CharField(max_length=10, blank=True, null=True)
    work_night = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    work_night_formatted = models.CharField(max_length=10, blank=True, null=True)
    work_deduction = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    work_deduction_formatted = models.CharField(max_length=10, blank=True, null=True)
    absent_overtime = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    absent_overtime_formatted = models.CharField(max_length=10, blank=True, null=True)
    status = models.SmallIntegerField(null=True)
    status_holiday = models.SmallIntegerField(default=0, null=True)
    status_accept_overtime = models.SmallIntegerField(default=0, null=True)
    status_day_off = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        hours_normal = int(self.normal_working_hours)
        minutes_normal = int((self.normal_working_hours - hours_normal) * 60)
        self.normal_working_hours_formatted = '{:02d}:{:02d}'.format(hours_normal, minutes_normal)
        hours_over = int(self.over_time)
        minutes_over = int((self.over_time - hours_over) * 60)
        hours_night = int(self.work_night)
        minutes_night = int((self.work_night - hours_night) * 60)
        hours_deduction = int(self.work_deduction)
        minutes_deduction = int((self.work_deduction - hours_deduction) * 60)
        hours_absent = int(self.absent_overtime)
        minutes_absent = int((self.absent_overtime - hours_absent) * 60 )
        self.date_persian = date2jalali(self.date)
        self.weekday_name = datetime.strftime(self.date, '%A')
        self.over_time_formatted = '{:02d}:{:02d}'.format(hours_over, minutes_over)
        self.work_night_formatted = '{:02d}:{:02d}'.format(hours_night, minutes_night)
        self.work_deduction_formatted = '{:02d}:{:02d}'.format(hours_deduction, minutes_deduction)
        self.absent_overtime_formatted = '{:02d}:{:02d}'.format(hours_absent, minutes_absent)

        if Holiday.objects.filter(date_holiday=self.date).exists():
            self.status_holiday=1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date', 'person']


class WorkRecordDaily(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کارمند")
    date_work = jmodels.jDateField(verbose_name="تاریخ", default=jdatetime.date.today)  # Changed from CharField to DateField for proper date handling
    arrived_time = models.TimeField(null=True, blank=True, verbose_name='ساعت ورود')
    departure_time = models.TimeField(null=True, blank=True, verbose_name='ساعت خروج')
    status = models.CharField(max_length=10, choices=LIST_ANSWER, default=PRESENT, verbose_name='وضعیت روزانه کارمند')
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")
    approval_status = models.TextField(blank=True, null=True, verbose_name="وضعیت تأیید")

    def clean(self):
            """ بررسی تکراری نبودن وضعیت برای یک روز (به جز مرخصی ساعتی). """
            if self.status != HOFF:  # اگر وضعیت مرخصی ساعتی نبود
                existing_record = WorkRecordDaily.objects.filter(
                    person=self.person,
                    date_work=self.date_work,
                    status=self.status
                ).exclude(pk=self.pk)  # بررسی رکوردهای دیگر (به جز همین رکورد در صورت ویرایش)
                
                if existing_record.exists():
                    raise ValidationError(f"وضعیت '{dict(LIST_ANSWER)[self.status]}' برای این تاریخ قبلاً ثبت شده است.")

    def save(self, *args, **kwargs):
            """ اگر شخص ثبت‌کننده همان شخصی باشد که در فیلد person آمده است، به‌صورت خودکار تأیید شود. """
            #if not self.pk:  # بررسی اینکه آیا رکورد جدید است
                #request = kwargs.pop('request', None)  # دریافت درخواست کاربر از `save` در فرم
            user = get_current_user()
            print('user>>>>>>>', user)
            if self.person == user and  self.departure_time is not None:
                self.is_approved = True  # تأیید خودکار اگر شخص ثبت‌کننده و `person` یکی باشند
                self.approval_status = f"امروز توسط {self.person.get_full_name()} مورد تأیید قرار گرفته است."  # توضیح وضعیت تأیید شده
            else:
                self.is_approved = False
                self.approval_status = f"وضعیت توسط کاربر مربوطه تایید نشده است."

            if self.status == DOFF and self.person == user:
                self.arrived_time = None
                self.departure_time = None
                self.is_approved = True
                self.approval_status = f" کاربر {self.person.get_full_name()} مرخصی روزانه بوده است."
            super().save(*args, **kwargs)


    # def _calculate_status(self):

    #     if self.arrived_time is None and self.departure_time is None:
    #         self.status = OFF

    #     """Calculate the employee's presence status based on arrival and departure times."""
    #     if self.arrived_time is not None and self.departure_time is not None:
    #         # تبدیل تاریخ شمسی به میلادی
    #         gregorian_date = self.date_work.togregorian()

    #         arrived_dt = datetime.combine(gregorian_date, self.arrived_time)
    #         departure_dt = datetime.combine(gregorian_date, self.departure_time)
    #         total_hours = (departure_dt - arrived_dt).total_seconds() / 3600

    #         # Set status to absent if arriving after 12 noon or working less than the required hours
    #         noon_time = time(12, 0)
    #         if self.arrived_time > noon_time or total_hours < 5:
    #             self.status = ABSENT
    #         else:
    #             self.status = PRESENT
    #     else:
    #         self.status = ABSENT


    class Meta:
        ordering = ['date_work', 'person']
        verbose_name = 'ثبت کارکرد روزانه'
        verbose_name_plural = 'ثبت کارکرد های روزانه'

    def __str__(self):
        return f"{self.person} on {self.date_work}"
    
    def get_date(self):
        return self.date_work.strftime('%Y/%m/%d')
    get_date.short_description="تاریخ"

    def get_weekday(self):
        """ دریافت نام روز هفته به فارسی """
        weekday_dict = {
            2: "دوشنبه",
            3: "سه‌شنبه",
            4: "چهارشنبه",
            5: "پنج‌شنبه",
            6: "جمعه",
            0: "شنبه",
            1: "یک‌شنبه"
        }
        return weekday_dict[self.date_work.weekday()]
    get_weekday.short_description = "روز هفته"




        

