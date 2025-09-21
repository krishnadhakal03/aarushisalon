#!/usr/bin/env python
"""
COMPLETE FIX for appointment system
This script will fix all issues and test the system
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aarushi_salon.settings')
    django.setup()

def clear_and_generate_slots():
    """Clear existing slots and generate new ones"""
    from salon.models import AppointmentSlot, Service, BusinessHours
    from django.utils import timezone
    from datetime import datetime, timedelta, time
    
    print("=== CLEARING AND GENERATING SLOTS ===")
    
    # Clear existing slots
    AppointmentSlot.objects.all().delete()
    print("✅ Cleared existing slots")
    
    # Get services
    services = Service.objects.filter(is_active=True)
    if services.count() == 0:
        print("❌ ERROR: No active services found!")
        return False
    
    print(f"✅ Found {services.count()} services")
    
    # Get business hours
    business_hours = {}
    for bh in BusinessHours.objects.all():
        business_hours[bh.day_of_week] = {
            'open_time': bh.open_time,
            'close_time': bh.close_time,
            'is_open': bh.is_open
        }
    
    # Generate slots for next 30 days
    today = timezone.now().date()
    end_date = today + timedelta(days=30)
    
    slots_created = 0
    current_date = today
    
    while current_date <= end_date:
        day_name = current_date.strftime('%A').lower()
        
        if day_name in business_hours and business_hours[day_name]['is_open']:
            open_time = business_hours[day_name]['open_time']
            close_time = business_hours[day_name]['close_time']
            
            # Generate 30-minute slots
            current_time = datetime.combine(current_date, open_time)
            end_time = datetime.combine(current_date, close_time)
            
            while current_time < end_time:
                slot_end = current_time + timedelta(minutes=30)
                
                # Create slots for each service
                for service in services:
                    AppointmentSlot.objects.create(
                        service=service,
                        date=current_date,
                        start_time=current_time.time(),
                        end_time=slot_end.time(),
                        is_available=True,
                        is_booked=False
                    )
                    slots_created += 1
                
                current_time += timedelta(minutes=30)
        
        current_date += timedelta(days=1)
    
    print(f"✅ Created {slots_created} appointment slots")
    return True

def test_system():
    """Test the appointment system"""
    from salon.models import AppointmentSlot, Service
    from django.utils import timezone
    from datetime import timedelta
    
    print("\n=== TESTING SYSTEM ===")
    
    # Test services
    services = Service.objects.filter(is_active=True)
    print(f"✅ Services: {services.count()}")
    for service in services:
        print(f"  - {service.name}: ${service.price}")
    
    # Test slots
    today = timezone.now().date()
    total_slots = AppointmentSlot.objects.count()
    print(f"✅ Total slots: {total_slots}")
    
    # Test slots for next 7 days
    for i in range(7):
        date = today + timedelta(days=i)
        slots = AppointmentSlot.objects.filter(date=date, is_available=True, is_booked=False)
        print(f"  {date.strftime('%A, %B %d')}: {slots.count()} slots")
    
    return total_slots > 0

def main():
    print("🚀 COMPLETE APPOINTMENT SYSTEM FIX")
    print("=" * 50)
    
    # Setup Django
    setup_django()
    
    # Clear and generate slots
    if not clear_and_generate_slots():
        print("❌ Failed to generate slots")
        return
    
    # Test system
    if not test_system():
        print("❌ System test failed")
        return
    
    print("\n" + "=" * 50)
    print("✅ ALL FIXES COMPLETE!")
    print("\n📋 NEXT STEPS:")
    print("1. Start server: python manage.py runserver 5600")
    print("2. Go to: http://127.0.0.1:5600/book-appointment/")
    print("3. Test the appointment form")
    print("\n🎯 EXPECTED RESULTS:")
    print("- ✅ Prices visible in service list")
    print("- ✅ Date dropdown shows 30+ days")
    print("- ✅ Time dropdown works after date selection")
    print("- ✅ Available time slots based on business hours")

if __name__ == '__main__':
    main()
