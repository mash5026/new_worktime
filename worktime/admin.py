from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from .models import WorkRecord, WorkRecordFinally, Holiday, WorkRecordDaily
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from django.contrib import messages
from django.db.models import Q
from jalali_date.widgets import AdminJalaliDateWidget
from jalali_date.admin import ModelAdminJalaliMixin
from .forms import WorkRecordDailyForm
from persons.signals import get_current_user



# @admin.action(description="رد کردن اضافه کاری")
# def reject_over_time(modeladmin,request,queryset):
#     reject = queryset.update(status_accept_overtime=1)
#     rows = queryset.filter(status_accept_overtime=1)
#     for i in range(len(rows)):
#           row = rows[i]
#           row.over_time = 0
#           row.save()
#     messages.success(request,f"{reject}   اضافه کاری رد شد")

# @admin.action(description='پذیرفتن مرخصی')
# def accept_day_off(modeladmin, request, queryset):
#     accept = queryset.update(status_day_off=0)
#     rows = queryset.filter(Q(status_day_off=0) | Q(work_deduction__gt=5))
#     for i in range(len(rows)):
#             row =  rows[i]
#             row.work_deduction = 0
#             row.save()
#     messages.success(request, f"{accept} مرخصی تایید شد")
    
    


# #@admin.action(description="موجود کردن ماشین ها")
# #def make_available_car(modeladmin,request,queryset):
#     #available = queryset.update(stock=True)
#     #messages.success(request,f"{available} ماشین به حالت موجود تغییر یافت.")


# #@admin.action(description="افزایش قیمت به میزان 20درصد")
# #def increase_price(modeladmin,request,queryset):
#     # all_price = list(queryset.values_list('price'))
#     # all_cars = queryset.all()
#     # numbers = queryset.count()
#     # new_price = list(map(lambda x: x[0]*1.2, all_price))
#     # for i in range(len(new_price)):
#     #     my_car = all_cars[i]
#     #     my_car.price = new_price[i]
#     #     my_car.save()
#     # new_price = queryset.update(price=F('price')+F('price')*0.2)
#     # messages.success(request, f"{new_price} قیمت به روز رسانی گردید.")


# @admin.register(WorkRecord)
# class WorkRecordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ('arrived_time', 'departure_time', 'person', 'date' , 'night_work', 'overtime_morning', 
# 'normal_working_hours', 'overtime_evening', 'work_nights', 'work_deduction_morning', 'work_deduction_evening',
# 'status')
#     list_filter = ('person',)
#     search_fields = ('person',)


# @admin.register(WorkRecordFinally)
# class WorkRecordFinallyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display  = ('person', 'date', 'date_persian', 'weekday_name',
#                      'normal_working_hours', 'normal_working_hours_formatted',
#                       'over_time', 'over_time_formatted', 
#                       'work_night', 'work_night_formatted',
#                      'work_deduction', 'work_deduction_formatted',
#                     'absent_overtime', 'absent_overtime_formatted',
#                     'status', 'status_holiday', 'status_accept_overtime', 'status_day_off')
#     list_filter = ('person',)
#     search_fields = ('person',)
#     actions = (reject_over_time, accept_day_off)

#     def colored_status(self, obj):
#         color = 'green'
#         if obj.status == 1:
#                     color = 'red'
#                     return format_html(

#             '<b style="background:{};">{}</b>',
#             color,
#             obj.status
#                        )
#         else:
#             return obj.status
#     colored_status.allow_tags = True
#     colored_status.short_description = 'Status'

#     # Add the method to the list_display
#     list_display = list(list_display)
#     list_display.remove('status')
#     list_display.append('colored_status')

#     def colored_status_holiday(self, obj):
#         color = 'green'
#         if obj.status_holiday == 1:
#                     color = 'yellow'
#                     return format_html(

#             '<b style="background:{};">{}</b>',
#             color,
#             obj.status_holiday
#                        )
#         else:
#             return obj.status_holiday
#     colored_status_holiday.allow_tags = True
#     colored_status_holiday.short_description = 'Status Holiday'

#     # Add the method to the list_display
#     list_display = list(list_display)
#     list_display.remove('status_holiday')
#     list_display.append('colored_status_holiday')


# @admin.register(Holiday)
# class AdminHoliday(admin.ModelAdmin):
#     list_display = ('date_holiday', 'event')


@admin.register(WorkRecordDaily)
class WorkRecordDailyAdmin(ModelAdminJalaliMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['person', 'date_work', 'get_weekday', 'arrived_time', 'departure_time', 'status', "is_approved", "approval_status"]
    list_filter = ('person',)
    search_fields = ('person',)
    form = WorkRecordDailyForm
    list_per_page = 25

    def get_form(self, request, obj=None, **kwargs):
        """ ارسال درخواست به فرم برای فیلتر کردن فیلد person """
        kwargs['form'] = WorkRecordDailyForm
        kwargs['form'].base_fields['person'].initial = request.user  # مقدار پیش‌فرض برای کاربر فعلی
        return super().get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'date_work':
            kwargs['widget'] = AdminJalaliDateWidget()
        
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # اگر کاربر ادمین باشد همه رکوردها را ببیند
        return qs.filter(person=request.user)
    
    def get_readonly_fields(self, request, obj=None):
  
        if obj:
            if obj.is_approved and not request.user.is_superuser:
                return ('person', 'date_work', 'get_weekday', 'arrived_time', 'departure_time', 'status', "is_approved", "approval_status")  
            elif not obj.is_approved and not request.user.is_superuser:
                return ('person', 'date_work', 'get_weekday', 'arrived_time', 'status', "approval_status")  # کاربران عادی فقط گزینه‌ی تأیید را ببینند
        return super().get_readonly_fields(request, obj)