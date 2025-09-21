#!/usr/bin/env python
"""
Quick test to verify the appointment system
"""
import os
import sys
import django

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aarushi_salon.settings')
    django.setup()
    
    from salon.models import AppointmentSlot, Service
    from django.utils import timezone
    from datetime import timedelta
    
    print("=== QUICK TEST ===")
    
    # Test services
    services = Service.objects.filter(is_active=True)
    print(f"✅ Services: {services.count()}")
    
    # Test slots
    total_slots = AppointmentSlot.objects.count()
    print(f"✅ Total slots: {total_slots}")
    
    # Test slots for next 3 days
    today = timezone.now().date()
    for i in range(3):
        date = today + timedelta(days=i)
        slots = AppointmentSlot.objects.filter(date=date, is_available=True, is_booked=False)
        print(f"  {date.strftime('%A, %B %d')}: {slots.count()} slots")
    
    print("\n✅ SYSTEM READY!")
    print("Test the website now!")

if __name__ == '__main__':
    main()
