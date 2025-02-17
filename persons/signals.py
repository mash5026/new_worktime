from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from threading import local
from .models import TimeStampedModel, CustomTable
from .models import AssetTransactionHistory
from .utils import database_table_exists
from django.db import connection


_user = local()

def set_current_user(user):
    _user.value = user

def get_current_user():
    return getattr(_user, 'value', None)

@receiver(pre_save)
def add_user_to_model(sender, instance, **kwargs):
    if issubclass(sender, TimeStampedModel):
        user = get_current_user()
        if user:
            if not instance.pk:  # اگر رکورد جدید است
                instance.created_by = user
            instance.updated_by = user

@receiver(pre_save, sender=AssetTransactionHistory)
def update_last_return_date(sender, instance, **kwargs):
    # اگر تاریخ تحویل برای رکورد جدید مشخص شده است، پس باید تاریخ تحویل رکورد قبلی را به روز کنیم.
    if instance.receive_date:
        # پیدا کردن آخرین رکورد مربوط به تراکنش اصلی
        last_history = AssetTransactionHistory.objects.filter(
            asset_transaction=instance.asset_transaction
        ).order_by('-receive_date').first()  # آخرین رکورد براساس تاریخ دریافت

        if last_history and last_history != instance:
            # به‌روزرسانی تاریخ تحویل آخرین رکورد
            last_history.return_date = instance.receive_date

            # برای جلوگیری از ایجاد حلقه بی‌پایان، از `update_fields` استفاده می‌کنیم
            last_history.save(update_fields=['return_date'])


@receiver(post_save, sender=AssetTransactionHistory)
def update_asset_transaction_receiver(sender, instance, created, **kwargs):
    if created:
        # اگر رکورد جدید ایجاد شد، فیلد receiver در AssetTransaction را بروزرسانی می‌کنیم.
        asset_transaction = instance.asset_transaction
        asset_transaction.receiver = instance.receiver
        asset_transaction.is_approved = False
        asset_transaction.approval_status = 'تأیید نشده'
        asset_transaction.save(update_fields=['receiver'])


@receiver(pre_delete, sender=CustomTable)
def delete_table_from_db(sender, instance, **kwargs):
    """ قبل از حذف مدل، جدول مرتبط را از دیتابیس حذف می‌کند """
    table_name = instance.table_name
    if database_table_exists(table_name):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f'DROP TABLE "{table_name}"')  # حذف جدول
                print(f'Table "{table_name}" dropped successfully!')
            except Exception as e:
                print(f"Error dropping table {table_name}: {e}")  # ثبت خطا در لاگ
    else:
        print(f'Table "{table_name}" does not exist.')
