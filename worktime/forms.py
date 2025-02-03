from django import forms
from .models import WorkRecordDaily
from persons.models import Personnel
from persons.middleware import get_current_user


class WorkRecordDailyForm(forms.ModelForm):
    """ فرم سفارشی برای فیلتر کردن فیلد person در پنل ادمین """
    class Meta:
        model = WorkRecordDaily
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # دریافت درخواست برای بررسی کاربر
        super().__init__(*args, **kwargs)
        user = get_current_user()
        print('user>>>', user)
        if user and not user.is_superuser:
            self.fields['person'].queryset = Personnel.objects.filter(person=user)