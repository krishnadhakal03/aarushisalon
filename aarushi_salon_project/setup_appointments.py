#!/usr/bin/env python
"""
Script to setup appointment system
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aarushi_salon.settings')
    django.setup()
    
    print("Setting up appointment system...")
    execute_from_command_line(['manage.py', 'setup_appointment_system'])
    
    print("Appointment system setup complete!")
