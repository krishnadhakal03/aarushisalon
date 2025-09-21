#!/usr/bin/env python
"""
Script to run Django migrations
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aarushi_salon.settings')
    django.setup()
    
    print("Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations', 'salon'])
    
    print("Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Migrations completed!")
