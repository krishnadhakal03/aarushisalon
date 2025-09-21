from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Service, AppointmentSlot
from .appointment_utils import get_appointment_availability_manager


@method_decorator(csrf_exempt, name='dispatch')
class GetAvailableSlotsView(View):
    """API view to get available appointment slots for multiple services and date"""
    
    def get(self, request):
        service_ids = request.GET.getlist('service_id')
        date_str = request.GET.get('date')
        
        if not service_ids or not date_str:
            return JsonResponse({'error': 'Service IDs and date are required'}, status=400)
        
        try:
            # Parse date
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Get services
            services = Service.objects.filter(id__in=service_ids, is_active=True)
            if not services.exists():
                return JsonResponse({'error': 'No valid services found'}, status=404)
            
            # Get available slots for all services
            availability_manager = get_appointment_availability_manager()
            all_slots = []
            
            for service in services:
                slots = availability_manager.get_available_slots(service.id, appointment_date, appointment_date)
                print(f"Service {service.name}: Found {slots.count()} slots")
                for slot in slots:
                    all_slots.append({
                        'start_time': slot.start_time.strftime('%H:%M'),
                        'end_time': slot.end_time.strftime('%H:%M'),
                        'display_time': slot.start_time.strftime('%I:%M %p'),
                        'service_id': service.id,
                        'service_name': service.name
                    })
            
            print(f"Total slots found: {len(all_slots)}")
            
            # Remove duplicates and sort by time
            unique_slots = {}
            for slot in all_slots:
                time_key = slot['start_time']
                if time_key not in unique_slots:
                    unique_slots[time_key] = slot
            
            slot_data = sorted(unique_slots.values(), key=lambda x: x['start_time'])
            print(f"Unique slots: {len(slot_data)}")
            
            return JsonResponse({
                'success': True,
                'slots': slot_data,
                'date': appointment_date.strftime('%A, %B %d, %Y')
            })
            
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class GetAvailableDatesView(View):
    """API view to get available dates for multiple services"""
    
    def get(self, request):
        service_ids = request.GET.getlist('service_id')
        
        if not service_ids:
            return JsonResponse({'error': 'Service IDs are required'}, status=400)
        
        try:
            # Get services
            services = Service.objects.filter(id__in=service_ids, is_active=True)
            if not services.exists():
                return JsonResponse({'error': 'No valid services found'}, status=404)
            
            # Get available dates for all services
            availability_manager = get_appointment_availability_manager()
            all_dates = set()
            
            for service in services:
                dates = availability_manager.get_available_dates(service.id)
                all_dates.update(dates)
            
            # If no common dates, return dates for any service
            if not all_dates:
                for service in services:
                    dates = availability_manager.get_available_dates(service.id)
                    all_dates.update(dates)
            
            # Format dates for frontend
            date_data = []
            for date in sorted(all_dates):
                date_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'display_date': date.strftime('%A, %B %d, %Y'),
                    'day_name': date.strftime('%A'),
                    'day_number': date.day,
                    'month_name': date.strftime('%B')
                })
            
            return JsonResponse({
                'success': True,
                'dates': date_data
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class CheckSlotAvailabilityView(View):
    """API view to check if a specific slot is available for multiple services"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            service_ids = data.get('service_ids', [])
            date_str = data.get('date')
            time_str = data.get('time')
            
            if not all([service_ids, date_str, time_str]):
                return JsonResponse({'error': 'Service IDs, date, and time are required'}, status=400)
            
            # Parse date and time
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time_str, '%H:%M').time()
            
            # Check availability for all services
            availability_manager = get_appointment_availability_manager()
            all_available = True
            
            for service_id in service_ids:
                is_available = availability_manager.is_slot_available(service_id, appointment_date, appointment_time)
                if not is_available:
                    all_available = False
                    break
            
            return JsonResponse({
                'success': True,
                'is_available': all_available
            })
            
        except ValueError as e:
            return JsonResponse({'error': f'Invalid date/time format: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_services_api(request):
    """API view to get all active services"""
    try:
        services = Service.objects.filter(is_active=True).select_related('category')
        
        service_data = []
        for service in services:
            service_data.append({
                'id': service.id,
                'name': service.name,
                'category': service.category.name,
                'price': float(service.price),
                'duration': service.duration,
                'duration_minutes': service.duration_minutes,
                'description': service.description
            })
        
        return JsonResponse({
            'success': True,
            'services': service_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
