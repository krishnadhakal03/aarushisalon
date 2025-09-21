from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, time
from salon.models import BusinessHours, AppointmentSlot, Service


class Command(BaseCommand):
    help = 'Setup business hours and generate appointment slots for the next month'

    def add_arguments(self, parser):
        parser.add_argument(
            '--regenerate-slots',
            action='store_true',
            help='Regenerate all appointment slots (this will delete existing slots)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up appointment system...'))

        # Setup default business hours
        self.setup_business_hours()
        
        # Generate appointment slots
        if options['regenerate_slots']:
            self.stdout.write(self.style.WARNING('Deleting existing appointment slots...'))
            AppointmentSlot.objects.all().delete()
        
        self.generate_appointment_slots()

        self.stdout.write(self.style.SUCCESS('Appointment system setup completed!'))

    def setup_business_hours(self):
        """Setup default business hours"""
        business_hours_data = [
            {'day_of_week': 'monday', 'is_open': False, 'open_time': time(10, 0), 'close_time': time(19, 0)},
            {'day_of_week': 'tuesday', 'is_open': True, 'open_time': time(10, 0), 'close_time': time(19, 0)},
            {'day_of_week': 'wednesday', 'is_open': True, 'open_time': time(10, 0), 'close_time': time(19, 0)},
            {'day_of_week': 'thursday', 'is_open': True, 'open_time': time(10, 0), 'close_time': time(19, 0)},
            {'day_of_week': 'friday', 'is_open': True, 'open_time': time(10, 0), 'close_time': time(19, 0)},
            {'day_of_week': 'saturday', 'is_open': True, 'open_time': time(10, 0), 'close_time': time(19, 0)},
            {'day_of_week': 'sunday', 'is_open': True, 'open_time': time(11, 0), 'close_time': time(17, 0)},
        ]

        for data in business_hours_data:
            business_hours, created = BusinessHours.objects.get_or_create(
                day_of_week=data['day_of_week'],
                defaults={
                    'is_open': data['is_open'],
                    'open_time': data['open_time'],
                    'close_time': data['close_time'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created business hours for {data["day_of_week"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Business hours for {data["day_of_week"]} already exist'))

    def generate_appointment_slots(self):
        """Generate appointment slots for the next month"""
        today = timezone.now().date()
        end_date = today + timedelta(days=30)  # Next month
        
        # Get all active services
        services = Service.objects.filter(is_active=True)
        if not services.exists():
            self.stdout.write(self.style.ERROR('No active services found. Please create services first.'))
            return

        # Get business hours
        business_hours = {bh.day_of_week: bh for bh in BusinessHours.objects.filter(is_active=True)}
        
        current_date = today
        slots_created = 0
        
        while current_date <= end_date:
            day_name = current_date.strftime('%A').lower()
            
            if day_name in business_hours and business_hours[day_name].is_open:
                bh = business_hours[day_name]
                slots_created += self.create_slots_for_date(current_date, bh, services)
            
            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(f'Created {slots_created} appointment slots'))

    def create_slots_for_date(self, date, business_hours, services):
        """Create appointment slots for a specific date"""
        slots_created = 0
        slot_duration = 60  # 60 minutes per slot
        
        # Calculate available time
        start_time = business_hours.open_time
        end_time = business_hours.close_time
        
        # Generate time slots
        current_time = start_time
        while current_time < end_time:
            slot_end_time = self.add_minutes_to_time(current_time, slot_duration)
            
            # Don't create slots that would go past closing time
            if slot_end_time <= end_time:
                for service in services:
                    # Check if slot already exists
                    if not AppointmentSlot.objects.filter(
                        date=date,
                        start_time=current_time,
                        service=service
                    ).exists():
                        AppointmentSlot.objects.create(
                            date=date,
                            start_time=current_time,
                            end_time=slot_end_time,
                            service=service,
                            is_available=True,
                            is_booked=False
                        )
                        slots_created += 1
            
            current_time = slot_end_time
        
        return slots_created

    def add_minutes_to_time(self, time_obj, minutes):
        """Add minutes to a time object"""
        datetime_obj = datetime.combine(datetime.today(), time_obj)
        new_datetime = datetime_obj + timedelta(minutes=minutes)
        return new_datetime.time()
