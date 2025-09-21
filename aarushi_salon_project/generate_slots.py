#!/usr/bin/env python
"""
Script to manually generate appointment slots
Run with: python generate_slots.py
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
    from datetime import datetime, timedelta, time
    
    print("=== GENERATING APPOINTMENT SLOTS ===")
    
    # Clear existing slots
    print("Clearing existing slots...")
    AppointmentSlot.objects.all().delete()
    
    # Get services
    services = Service.objects.filter(is_active=True)
    if services.count() == 0:
        print("❌ ERROR: No active services found!")
        return
    
    print(f"Found {services.count()} services")
    
    # Get business hours
    business_hours = {}
    for bh in BusinessHours.objects.all():
        business_hours[bh.day_of_week] = {
            'open_time': bh.open_time,
            'close_time': bh.close_time,
            'is_open': bh.is_open
        }
    
    print("Business hours:")
    for day, hours in business_hours.items():
        if hours['is_open']:
            print(f"  {day}: {hours['open_time']} - {hours['close_time']}")
        else:
            print(f"  {day}: CLOSED")
    
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
                    slot = AppointmentSlot.objects.create(
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
    
    print(f"\n✅ Created {slots_created} appointment slots")
    
    # Verify slots
    print("\n=== VERIFYING SLOTS ===")
    for i in range(7):
        date = today + timedelta(days=i)
        slots = AppointmentSlot.objects.filter(date=date, is_available=True, is_booked=False)
        print(f"{date.strftime('%A, %B %d')}: {slots.count()} slots")
        
        if slots.count() > 0 and i < 3:
            for slot in slots[:5]:
                print(f"  - {slot.start_time.strftime('%I:%M %p')} ({slot.service.name})")
    
    print("\n=== DONE ===")
    print("Now test the website!")

if __name__ == '__main__':
    main()
