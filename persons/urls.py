from django.urls import path
from .views import validate_nationalid, check_nationalid, validate_mobile, check_mobile_exists

urlpatterns = [
    path('check-nationalid/<str:nationalid>/', check_nationalid, name='check_nationalid'),
    path('validate-nationalid/<str:nationalid>/', validate_nationalid, name='validate_nationalid'),
    path('validate-mobile/<str:mobile>/', validate_mobile, name='validate_mobile'),
    path('check-mobile/<str:mobile>/', check_mobile_exists, name='check_mobile_exists'),
]