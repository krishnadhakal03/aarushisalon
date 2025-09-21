from django.utils import timezone
from datetime import datetime, timedelta, time
from .models import BusinessHours, AppointmentSlot, Service


class AppointmentAvailabilityManager:
    """Manages appointment availability and slot generation"""
    
    def __init__(self):
        self.business_hours = self._get_business_hours()
    
    def _get_business_hours(self):
        """Get business hours configuration"""
        return {bh.day_of_week: bh for bh in BusinessHours.objects.filter(is_active=True)}
    
    def get_available_slots(self, service_id, start_date=None, end_date=None):
        """Get available appointment slots for a service within date range"""
        if not start_date:
            start_date = timezone.now().date()
        if not end_date:
            end_date = start_date + timedelta(days=30)
        
        # Get available slots
        slots = AppointmentSlot.objects.filter(
            service_id=service_id,
            date__gte=start_date,
            date__lte=end_date,
            is_available=True,
            is_booked=False
        ).order_by('date', 'start_time')
        
        return slots
    
    def get_available_slots_by_date(self, service_id, date):
        """Get available slots for a specific date"""
        return self.get_available_slots(service_id, date, date)
    
    def get_available_dates(self, service_id, start_date=None, end_date=None):
        """Get dates that have available slots"""
        slots = self.get_available_slots(service_id, start_date, end_date)
        dates = slots.values_list('date', flat=True).distinct().order_by('date')
        return dates
    
    def is_slot_available(self, service_id, date, start_time):
        """Check if a specific slot is available"""
        try:
            slot = AppointmentSlot.objects.get(
                service_id=service_id,
                date=date,
                start_time=start_time
            )
            return slot.is_available_for_booking
        except AppointmentSlot.DoesNotExist:
            return False
    
    def book_slot(self, service_id, date, start_time, appointment):
        """Book a specific slot"""
        try:
            slot = AppointmentSlot.objects.get(
                service_id=service_id,
                date=date,
                start_time=start_time
            )
            
            if slot.is_available_for_booking:
                slot.appointment = appointment
                slot.is_booked = True
                slot.save()
                return True
            return False
        except AppointmentSlot.DoesNotExist:
            return False
    
    def cancel_slot_booking(self, appointment):
        """Cancel a slot booking"""
        if appointment.appointment_slot:
            slot = appointment.appointment_slot
            slot.appointment = None
            slot.is_booked = False
            slot.save()
            return True
        return False
    
    def generate_slots_for_service(self, service, start_date, end_date):
        """Generate appointment slots for a service within date range"""
        current_date = start_date
        slots_created = 0
        
        while current_date <= end_date:
            day_name = current_date.strftime('%A').lower()
            
            if day_name in self.business_hours and self.business_hours[day_name].is_open:
                bh = self.business_hours[day_name]
                slots_created += self._create_slots_for_date(current_date, bh, service)
            
            current_date += timedelta(days=1)
        
        return slots_created
    
    def _create_slots_for_date(self, date, business_hours, service):
        """Create appointment slots for a specific date and service"""
        slots_created = 0
        slot_duration = 60  # 60 minutes per slot
        
        start_time = business_hours.open_time
        end_time = business_hours.close_time
        
        current_time = start_time
        while current_time < end_time:
            slot_end_time = self._add_minutes_to_time(current_time, slot_duration)
            
            if slot_end_time <= end_time:
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
    
    def _add_minutes_to_time(self, time_obj, minutes):
        """Add minutes to a time object"""
        datetime_obj = datetime.combine(datetime.today(), time_obj)
        new_datetime = datetime_obj + timedelta(minutes=minutes)
        return new_datetime.time()
    
    def get_business_hours_for_date(self, date):
        """Get business hours for a specific date"""
        day_name = date.strftime('%A').lower()
        return self.business_hours.get(day_name)
    
    def is_business_day(self, date):
        """Check if a date is a business day"""
        day_name = date.strftime('%A').lower()
        return day_name in self.business_hours and self.business_hours[day_name].is_open


def get_appointment_availability_manager():
    """Get an instance of AppointmentAvailabilityManager"""
    return AppointmentAvailabilityManager()
