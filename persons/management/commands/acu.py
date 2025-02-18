from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from persons.resources import ACK

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('key', type=str)

    def handle(self, *args, **kwargs):
        key = kwargs['key']

        if key != ACK:
            self.stdout.write(self.style.ERROR("❌ کلید وارد شده اشتباه است!"))
            return

        updated_count = User.objects.filter(is_active=False).update(is_active=True)
        self.stdout.write(self.style.SUCCESS(f"✅ {updated_count} کاربر با موفقیت فعال شد."))