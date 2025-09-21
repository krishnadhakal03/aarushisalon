#!/usr/bin/env python
"""
Script to fix appointment system issues
Run with: python fix_appointments.py
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aarushi_salon.settings')
    django.setup()
    
    from salon.models import AppointmentSlot, Service, BusinessHours
    from django.utils import timezone
    from datetime import timedelta
    
    print("=== CHECKING APPOINTMENT SYSTEM ===")
    print(f"Services: {Service.objects.count()}")
    print(f"Business Hours: {BusinessHours.objects.count()}")
    print(f"Appointment Slots: {AppointmentSlot.objects.count()}")
    
    # Check if we have services
    services = Service.objects.filter(is_active=True)
    if services.count() == 0:
        print("\n❌ ERROR: No active services found!")
        print("Please add some services in the admin panel first.")
        return
    
    print(f"\n✅ Found {services.count()} active services:")
    for service in services:
        print(f"  - {service.name}: ${service.price} ({service.duration})")
    
    # Check if we have appointment slots
    if AppointmentSlot.objects.count() == 0:
        print("\n=== GENERATING APPOINTMENT SLOTS ===")
        try:
            execute_from_command_line(['manage.py', 'setup_appointment_system'])
            print(f"✅ Generated {AppointmentSlot.objects.count()} appointment slots")
        except Exception as e:
            print(f"❌ Error generating slots: {e}")
            return
    else:
        print(f"\n✅ Found {AppointmentSlot.objects.count()} existing appointment slots")
    
    # Check slots for next few days
    print("\n=== CHECKING AVAILABLE SLOTS ===")
    today = timezone.now().date()
    
    for i in range(7):  # Check next 7 days
        date = today + timedelta(days=i)
        slots = AppointmentSlot.objects.filter(date=date, is_available=True, is_booked=False)
        print(f"{date.strftime('%A, %B %d')}: {slots.count()} available slots")
        
        if slots.count() > 0 and i < 3:  # Show details for first 3 days
            for slot in slots[:5]:  # Show first 5 slots
                print(f"  - {slot.start_time.strftime('%I:%M %p')} to {slot.end_time.strftime('%I:%M %p')} ({slot.service.name})")
    
    print("\n=== TESTING WEBSITE ===")
    print("1. Start server: python manage.py runserver 5600")
    print("2. Go to: http://127.0.0.1:5600/book-appointment/")
    print("3. Check if prices show and time slots work")
    
    print("\n=== DONE ===")

if __name__ == '__main__':
    main()
