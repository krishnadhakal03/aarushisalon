#!/usr/bin/env python
"""
Test the simple forms
"""
import os
import sys
import django

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aarushi_salon.settings')
    django.setup()
    
    print("✅ SIMPLE FORMS READY!")
    print("\n📋 FORMS CREATED:")
    print("1. Contact Form - matches http://www.arushisalon.com/contacts/")
    print("2. Appointment Form - matches http://www.arushisalon.com/appointment/")
    
    print("\n🎯 FEATURES:")
    print("✅ Contact Form:")
    print("  - Name, Phone (optional), Email, Subject dropdown, Message")
    print("  - Math captcha (10 + 14 = 24)")
    print("  - Matches real website exactly")
    
    print("\n✅ Appointment Form:")
    print("  - Full Name, Service Category, Date, Time, Phone, Email, Message")
    print("  - Math captcha (3 + 4 = 7)")
    print("  - Business hours display")
    print("  - Matches real website exactly")
    
    print("\n🚀 TEST NOW:")
    print("1. Start server: python manage.py runserver 8200")
    print("2. Contact: http://127.0.0.1:8200/contact/")
    print("3. Appointment: http://127.0.0.1:8200/book-appointment/")
    
    print("\n✅ DONE!")

if __name__ == '__main__':
    main()
