#!/usr/bin/env python
"""
Script to check and fix appointment system issues
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aarushi_salon.settings')
    django.setup()
    
    from salon.models import AppointmentSlot, Service, BusinessHours
    
    print("=== CHECKING APPOINTMENT SYSTEM ===")
    print(f"Services: {Service.objects.count()}")
    print(f"Business Hours: {BusinessHours.objects.count()}")
    print(f"Appointment Slots: {AppointmentSlot.objects.count()}")
    
    if AppointmentSlot.objects.count() == 0:
        print("\n=== SETTING UP APPOINTMENT SYSTEM ===")
        execute_from_command_line(['manage.py', 'setup_appointment_system'])
        print(f"Appointment Slots after setup: {AppointmentSlot.objects.count()}")
    
    print("\n=== CHECKING SERVICES ===")
    for service in Service.objects.filter(is_active=True):
        print(f"- {service.name}: ${service.price} ({service.duration})")
    
    print("\n=== CHECKING SLOTS FOR TODAY ===")
    from django.utils import timezone
    today = timezone.now().date()
    slots_today = AppointmentSlot.objects.filter(date=today, is_available=True, is_booked=False)
    print(f"Available slots today: {slots_today.count()}")
    
    if slots_today.count() > 0:
        for slot in slots_today[:5]:  # Show first 5
            print(f"  - {slot.start_time} to {slot.end_time} ({slot.service.name})")
    
    print("\n=== DONE ===")
