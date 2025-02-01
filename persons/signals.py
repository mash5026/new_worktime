from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from threading import local
from .models import TimeStampedModel


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
