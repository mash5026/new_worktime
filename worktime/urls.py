from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('insert-records/', views.insert_records, name='insert_records'),
    path('holiday/', views.show_holiday, name='show_holiday'),
]