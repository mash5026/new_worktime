from collections.abc import Iterable
from django.db import models
from .utils import LIST_ANSWER, PRESENT, ABSENT
from datetime import datetime, time
from django_jalali.db import models as jmodels
from jalali_date import datetime2jalali, date2jalali
import jdatetime

# Assuming LIST_ANSWER and status choices are defined elsewhere as mentioned
ABSENT = 'A'
PRESENT = 'P'
LIST_ANSWER = [(ABSENT, 'Absent'), (PRESENT, 'Present')]

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
        self.over_time_formatted = '{:02d}:{:02d}'.format(hours_over, minutes_over)
        self.work_night_formatted = '{:02d}:{:02d}'.format(hours_night, minutes_night)
        self.work_deduction_formatted = '{:02d}:{:02d}'.format(hours_deduction, minutes_deduction)
        self.absent_overtime_formatted = '{:02d}:{:02d}'.format(hours_absent, minutes_absent)

        if Holiday.objects.filter(date_holiday=self.date).exists():
            self.status_holiday=1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date', 'person']




        

