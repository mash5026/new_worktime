from django.urls import path
from .views import validate_nationalid, check_nationalid

urlpatterns = [
    path('check-nationalid/<str:nationalid>/', check_nationalid, name='check_nationalid'),
    path('validate-nationalid/<str:nationalid>/', validate_nationalid, name='validate_nationalid')
]