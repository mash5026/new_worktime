from django.contrib import admin
from django.utils.html import format_html
from .models import AssetTransactionHistory, Personnel, EducationalDocument, TrainingCertificate, InsuranceRecords, EmploymentHistory, TypeDocRecords, AssetTransaction, Asset, Brand, NameAsset
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date.widgets import AdminJalaliDateWidget
from iranian_cities.admin import IranianCitiesAdmin
from jalali_date.admin import ModelAdminJalaliMixin
from import_export.admin import ImportExportModelAdmin
from .forms import EducationalDocumentForm, TrainingCertificateForm, InsuranceRecordsForm, EmploymentHistoryForm



class TypeDocRecordsInline(admin.TabularInline):  # یا admin.StackedInline برای طراحی متفاوت
    model = TypeDocRecords
    extra = 1  # تعداد رکوردهایی که به صورت پیش‌فرض نمایش داده می‌شود
    fields = ('name_type', 'name_doc', 'serial_number','certificate_file')  # فیلدهای مورد نمایش در فرم اینلاین
    #readonly_fields = ('name_type', 'name_doc', 'certificate_file')  # در صورت نیاز می‌توانید فیلدهای فقط خواندنی تنظیم کنید

class EducationalDocumentInline(admin.TabularInline):  # یا admin.StackedInline برای طراحی متفاوت
    model = EducationalDocument
    extra = 1  # تعداد رکوردهایی که به صورت پیش‌فرض نمایش داده می‌شود
    fields = ('name_doc', 'document_file')  # فیلدهای مورد نمایش در فرم اینلاین
    #readonly_fields = ('name_doc', 'document_file')  # در صورت نیاز می‌توانید فیلدهای فقط خواندنی تنظیم کنید

# کلاس اینلاین برای گواهینامه‌های آموزشی
class TrainingCertificateInline(admin.TabularInline):  # یا admin.StackedInline برای طراحی متفاوت
    model = TrainingCertificate
    extra = 1  # تعداد رکوردهایی که به صورت پیش‌فرض نمایش داده می‌شود
    fields = ('name_doc', 'certificate_file')  # فیلدهای مورد نمایش در فرم اینلاین
    #readonly_fields = ('name_doc', 'certificate_file')

class InsuranceRecordsInline(admin.TabularInline):  # یا admin.StackedInline برای طراحی متفاوت
    model = InsuranceRecords
    extra = 1  # تعداد رکوردهایی که به صورت پیش‌فرض نمایش داده می‌شود
    fields = ('name_doc', 'certificate_file')  # فیلدهای مورد نمایش در فرم اینلاین
    #readonly_fields = ('name_doc', 'certificate_file')

class EmploymentHistoryInline(admin.TabularInline):  # Or admin.StackedInline for a different layout
    model = EmploymentHistory
    extra = 1  # Number of empty forms displayed initially
    fields = ['company_name', 'job_title', 'work_experience', 'organizational_unit']
    #readonly_fields = ['start_date', 'end_date']  # If you want some fields to be readonly
    show_change_link = True  # Allows a link to edit employment history

class AssetTransactionHistoryInline(ModelAdminJalaliMixin, admin.TabularInline):
    model = AssetTransactionHistory
    extra = 1

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'receive_date' or db_field.name =='return_date':
            kwargs['widget'] = AdminJalaliDateWidget()  # استفاده از ویجت تاریخ شمسی
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Personnel)
class PersonnelAdmin(ImportExportModelAdmin, ModelAdminJalaliMixin, IranianCitiesAdmin, admin.ModelAdmin):
    list_display = ('profile_image_preview', 'first_name', 'last_name', 'NATIONALID', 'get_date', 'education_level', 'Insurance_records',
                    'insurance_number', 'job_title', 'nationality', 'religion', 'sect', 'marital_status', 'weight', 'height',
                    'military_service', 'hair_color', 'organizational_title',  'organizational_unit', 'employment_status')
    search_fields = ('person', 'NATIONALID')
    list_filter = ('birth_date',)
    inlines = [TypeDocRecordsInline, EducationalDocumentInline, TrainingCertificateInline, InsuranceRecordsInline, EmploymentHistoryInline]
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by', 'first_name', 'last_name')
    class Media:
        js = ('nationalid_check.js', 'check_mobile.js',)

    fieldsets = [
        ('اطلاعات فردی', {
            'fields': [('person', 'NATIONALID', 'identity_number'),
                       ('father_name', 'birth_places', 'birth_certificate_issue_city'),
                       ('address', 'phone_number', 'callphone')],
            'classes': ['wide'],
        }),
        ('اطلاعات شغلی', {
            'fields': [('job_title', 'organizational_unit', 'organizational_title'),
                       ('employment_status', 'account_number', 'sheba_number'),
                       ('card_number',)],
        }),
        ('اطلاعات تحصیلی', {
            'fields': [('education_level', 'Insurance_records', 'insurance_number')],
        }),
        ('وضعیت نظام وظیفه', {
            'fields': [('military_service', 'military_service_front', 'military_service_back')],
        }),
        ('اطلاعات هویتی', {
            'fields': [('nationality', 'religion', 'sect'),
                       ('marital_status', 'number_of_children', 'birth_date')],
        }),
        ('مشخصات ظاهری', {
            'fields': [('weight', 'height', 'hair_color'),
                       ('profile_image',)],
        }),
        ('مدارک و اسناد', {
            'fields': [('national_card_file_front', 'national_card_file_back'),
                       ('resume_file', 'owner_file')],
        }),
    ]

    def first_name(self, obj):
        return obj.first_name

    def last_name(self, obj):
        return obj.last_name
    
    first_name.admin_order_field = 'person__first_name'
    last_name.admin_order_field = 'person__last_name'
    first_name.short_description = "نام"
    last_name.short_description = "نام خانوادگی"

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'birth_date':
            kwargs['widget'] = AdminJalaliDateWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.profile_image.url)
        return "بدون عکس"

    profile_image_preview.short_description = "عکس پرسنلی"

    def get_created_by(self, obj):
        """Return the username of the user who created the record"""
        return obj.created_by.username if obj.created_by else None
    get_created_by.short_description = 'ثبت‌کننده'

    def get_updated_by(self, obj):
        """Return the username of the user who last updated the record"""
        return obj.updated_by.username if obj.updated_by else None
    get_updated_by.short_description = 'بروزرسانی‌کننده'

    def save_model(self, request, obj, form, change):
        """
        Automatically populate the 'created_by' and 'updated_by' fields.
        """
        if not obj.pk:  # This is a new record
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # اگر کاربر ادمین باشد همه رکوردها را ببیند
        return qs.filter(person=request.user)


@admin.register(EducationalDocument)
class EducationalDocumentAdmin(admin.ModelAdmin):
    form = EducationalDocumentForm
    list_display = ('personnel', 'name_doc','document_file')
    search_fields = ('personnel__first_name', 'personnel__last_name')
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # اگر کاربر ادمین باشد همه رکوردها را ببیند
        return qs.filter(personnel__person=request.user)


@admin.register(TrainingCertificate)
class TrainingCertificateAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'name_doc','certificate_file')
    search_fields = ('personnel__first_name', 'personnel__last_name')
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by')
    form = TrainingCertificateForm
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # اگر کاربر ادمین باشد همه رکوردها را ببیند
        return qs.filter(personnel__person=request.user)


@admin.register(InsuranceRecords)
class InsuranceRecordsAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'name_doc','certificate_file')
    search_fields = ('personnel__first_name', 'personnel__last_name')
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by')
    form = InsuranceRecordsForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # اگر کاربر ادمین باشد همه رکوردها را ببیند
        return qs.filter(personnel__person=request.user)    

@admin.register(TypeDocRecords)
class TypeDocRecordsAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'name_type','name_doc', 'serial_number', 'certificate_file')
    search_fields = ('personnel__first_name', 'personnel__last_name')
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # اگر کاربر ادمین باشد همه رکوردها را ببیند
        return qs.filter(personnel__person=request.user)
    

@admin.register(EmploymentHistory)
class EmploymentHistoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['personnel', 'company_name', 'job_title', 'work_experience', 'organizational_unit']
    search_fields = ['company_name', 'job_title']
    list_filter = ['job_title', 'organizational_unit']
    form = EmploymentHistoryForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # اگر کاربر ادمین باشد همه رکوردها را ببیند
        return qs.filter(personnel__person=request.user)
    

@admin.register(AssetTransaction)
class AssetTransactionAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("asset", "serial_number", "receiver", "giver", "receive_date", "return_date", "description")
    search_fields = ("serial_number", "receiver__username", "giver__username", "asset__name")
    list_filter = ("receive_date", "return_date", "receiver")
    inlines = [AssetTransactionHistoryInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # ابرکاربر همه‌ی اطلاعات را می‌بیند
        return qs.filter(receiver=request.user)  # کاربران فقط اموال خودشان را ببینند

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "receiver" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.received_assets.all()  # فقط کاربر فعلی را نمایش دهد
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'receive_date' or db_field.name == 'return_date':
            kwargs['widget'] = AdminJalaliDateWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(NameAsset)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "price")
    search_fields = ("name", "brand__name", "model_name")
    list_filter = ("brand",)

# @admin.register(AssetTransactionHistory)
# class AssetTransactionHistoryAdmin(ModelAdminJalaliMixin,  admin.ModelAdmin):
#     list_display = ('asset_transaction', 'receiver', 'receive_date', 'description')
#     search_fields = ('asset_transaction__asset__name', 'receiver__username')
#     list_filter = ('receive_date', 'receiver')

#     def formfield_for_dbfield(self, db_field, request, **kwargs):
#         if db_field.name == 'receive_date':
#             kwargs['widget'] = AdminJalaliDateWidget()
#         return super().formfield_for_dbfield(db_field, request, **kwargs)