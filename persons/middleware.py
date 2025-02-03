import threading
from django.http import HttpResponse
from django.db import transaction


_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, "user", None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = request.user if request.user.is_authenticated else None
        response = self.get_response(request)
        return response
    
    
class LicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        from .models import License
        # چک کردن انقضای لایسنس فقط در صورت درخواست از صفحه اصلی یا صفحات دیگر که نیاز به بررسی دارند
        if not request.path.startswith('/admin/'):  # اختیاری، فقط صفحات مورد نظر بررسی می‌شود
            try:
                license = License.objects.latest('activation_date')
                if license.is_expired():
                    
                    
                    with transaction.atomic():
                        # حذف تمام رکوردها در دیتابیس
                        # برای جلوگیری از حذف غیرقابل بازگشت داده‌ها بهتر است قبل از حذف از کاربر تایید بگیرید.
                        License.objects.all().delete()  # حذف تمام رکوردها

                    return HttpResponse("لایسنس شما منقضی شده است و داده‌ها حذف شده‌اند.", status=403)
            except License.DoesNotExist:
                # اگر لایسنس وجود نداشته باشد، هیچ کاری انجام نمی‌دهیم
                pass

        # اگر لایسنس منقضی نشده باشد، درخواست به‌صورت عادی پردازش می‌شود
        response = self.get_response(request)
        return response
