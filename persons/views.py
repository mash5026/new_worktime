from django.shortcuts import render
from .utils import IsnationalCode
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Personnel

# Create your views here.

def check_nationalid(request, nationalid):
    # Check if the nationalid already exists in the Profile model
    exists = Personnel.objects.filter(NATIONALID=nationalid).exists()
    return JsonResponse({'exists': exists})

def validate_nationalid(request, nationalid):
    # Check if the national ID is valid using the IsnationalCode function
    try:
        if not IsnationalCode(nationalid):
            return JsonResponse({'valid': False})
        return JsonResponse({'valid': True})
    except ValidationError:
        return JsonResponse({'valid': False})
