#!/usr/bin/env python
"""
Script to create and apply migration for ContactMessage model
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aarushi_salon.settings')
    django.setup()
    
    print("=== CREATING CONTACT MESSAGE MIGRATION ===")
    
    # Create migration
    print("Creating migration for ContactMessage model...")
    execute_from_command_line(['manage.py', 'makemigrations', 'salon'])
    
    # Apply migration
    print("Applying migration...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ ContactMessage model migration complete!")
    print("\n📋 WHAT'S NEW:")
    print("✅ Contact form now stores data in database")
    print("✅ Admin panel shows contact messages")
    print("✅ Messages have status tracking (new, read, replied, closed)")
    print("✅ Search and filter messages by name, email, subject")
    
    print("\n🚀 TEST NOW:")
    print("1. Start server: python manage.py runserver 8200")
    print("2. Submit contact form: http://127.0.0.1:8200/contact/")
    print("3. View messages in admin: http://127.0.0.1:8200/admin/")

if __name__ == '__main__':
    main()
