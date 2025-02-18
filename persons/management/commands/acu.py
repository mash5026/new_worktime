from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "فعال‌سازی مجدد تمامی کاربران غیرفعال"

    def handle(self, *args, **kwargs):
        updated_count = User.objects.filter(is_active=False).update(is_active=True)
        self.stdout.write(self.style.SUCCESS(f'{updated_count} کاربر فعال شد.'))