from django import forms
from .models import EducationalDocument, Personnel, TrainingCertificate, InsuranceRecords, EmploymentHistory

from persons.middleware import get_current_user


class EducationalDocumentForm(forms.ModelForm):
    """ فرم سفارشی برای فیلتر کردن فیلد person در پنل ادمین """
    class Meta:
        model = EducationalDocument
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # دریافت درخواست برای بررسی کاربر
        super().__init__(*args, **kwargs)
        user = get_current_user()
        print('user>>>', user)
        if user and not user.is_superuser:
            self.fields['personnel'].queryset = Personnel.objects.filter(person=user)


class TrainingCertificateForm(forms.ModelForm):
    """ فرم سفارشی برای فیلتر کردن فیلد person در پنل ادمین """
    class Meta:
        model = TrainingCertificate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # دریافت درخواست برای بررسی کاربر
        super().__init__(*args, **kwargs)
        user = get_current_user()
        print('user>>>', user)
        if user and not user.is_superuser:
            self.fields['personnel'].queryset = Personnel.objects.filter(person=user)


class InsuranceRecordsForm(forms.ModelForm):
    """ فرم سفارشی برای فیلتر کردن فیلد person در پنل ادمین """
    class Meta:
        model = InsuranceRecords
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # دریافت درخواست برای بررسی کاربر
        super().__init__(*args, **kwargs)
        user = get_current_user()
        print('user>>>', user)
        if user and not user.is_superuser:
            self.fields['personnel'].queryset = Personnel.objects.filter(person=user)


class EmploymentHistoryForm(forms.ModelForm):
    """ فرم سفارشی برای فیلتر کردن فیلد person در پنل ادمین """
    class Meta:
        model = EmploymentHistory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # دریافت درخواست برای بررسی کاربر
        super().__init__(*args, **kwargs)
        user = get_current_user()
        print('user>>>', user)
        if user and not user.is_superuser:
            self.fields['personnel'].queryset = Personnel.objects.filter(person=user)