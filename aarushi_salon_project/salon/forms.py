from django import forms
from django.utils import timezone
from datetime import datetime, timedelta
from .models import CustomerFeedback, Appointment, Service, AppointmentSlot, AppointmentService
from .appointment_utils import get_appointment_availability_manager

class CustomerFeedbackForm(forms.ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = ['name', 'email', 'phone', 'service_received', 'rating', 'feedback', 'is_anonymous']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number (optional)'
            }),
            'service_received': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Hair Styling, Facial Treatment, etc.',
                'required': True
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your experience...',
                'rows': 4,
                'required': True
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'service_received': 'Service Received',
            'rating': 'Rating',
            'feedback': 'Your Feedback',
            'is_anonymous': 'Submit anonymously'
        }
        help_texts = {
            'name': 'Your name will be displayed with your feedback',
            'email': 'We will use this to contact you if needed',
            'phone': 'Optional - for follow-up if needed',
            'service_received': 'Which service did you receive?',
            'rating': 'How would you rate your experience?',
            'feedback': 'Share your experience with other customers',
            'is_anonymous': 'Check this to hide your name from public display'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make phone field not required
        self.fields['phone'].required = False


class AppointmentBookingForm(forms.ModelForm):
    """Form for booking appointments with dynamic slot selection"""
    
    class Meta:
        model = Appointment
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special requests or notes...',
                'rows': 3
            })
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'message': 'Special Requests (Optional)'
        }

    # Custom fields for slot selection
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'id': 'id_services'
        }),
        label='Select Services',
        required=True
    )
    
    appointment_date = forms.DateField(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_appointment_date'
        }),
        label='Select Date',
        required=True
    )
    
    appointment_time = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_appointment_time'
        }),
        label='Select Time',
        required=False,  # Allow submission without time selection
        choices=[('', 'Select a time slot')]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up service choices
        self.fields['services'].queryset = Service.objects.filter(is_active=True)
        
        # Set up date choices (next 30 days)
        today = timezone.now().date()
        end_date = today + timedelta(days=30)
        
        date_choices = [('', 'Select a date')]
        current_date = today
        while current_date <= end_date:
            date_choices.append((current_date, current_date.strftime('%A, %B %d, %Y')))
            current_date += timedelta(days=1)
        
        self.fields['appointment_date'].widget.choices = date_choices
        
        # Initialize time choices
        self.fields['appointment_time'].choices = [('', 'Select a time slot')]

    def clean_services(self):
        """Validate services selection"""
        services = self.cleaned_data.get('services')
        if not services:
            raise forms.ValidationError("Please select at least one service.")
        return services

    def clean_appointment_time(self):
        """Validate appointment time selection"""
        appointment_time = self.cleaned_data.get('appointment_time')
        appointment_date = self.cleaned_data.get('appointment_date')
        services = self.cleaned_data.get('services')
        
        # If no time selected, that's okay - we'll call the customer
        if not appointment_time:
            return appointment_time
        
        if appointment_time and appointment_date and services:
            # Check if the selected slot is still available for any of the services
            availability_manager = get_appointment_availability_manager()
            for service in services:
                if not availability_manager.is_slot_available(service.id, appointment_date, appointment_time):
                    raise forms.ValidationError(f"Time slot is no longer available for {service.name}. Please select another time.")
        
        return appointment_time

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        services = cleaned_data.get('services')
        
        if appointment_date and appointment_time and services:
            # Check if slots exist and are available for all services
            for service in services:
                try:
                    slot = AppointmentSlot.objects.get(
                        service=service,
                        date=appointment_date,
                        start_time=appointment_time
                    )
                    if not slot.is_available_for_booking:
                        raise forms.ValidationError(f"Time slot is no longer available for {service.name}. Please select another time.")
                except AppointmentSlot.DoesNotExist:
                    raise forms.ValidationError(f"Invalid time slot for {service.name}.")
        
        return cleaned_data

    def save(self, commit=True):
        """Save the appointment with slot information and services"""
        appointment = super().save(commit=False)
        
        if commit:
            # Set the appointment date and time from the form fields
            appointment.preferred_date = self.cleaned_data['appointment_date']
            appointment.preferred_time = self.cleaned_data['appointment_time']
            
            # Save the appointment first
            appointment.save()
            
            # Add selected services
            services = self.cleaned_data['services']
            for service in services:
                AppointmentService.objects.create(
                    appointment=appointment,
                    service=service
                )
            
            # Find and assign the appointment slot (use first service for slot)
            if services:
                try:
                    slot = AppointmentSlot.objects.get(
                        service=services[0],
                        date=appointment.preferred_date,
                        start_time=appointment.preferred_time
                    )
                    appointment.appointment_slot = slot
                    appointment.save()
                except AppointmentSlot.DoesNotExist:
                    pass  # Handle gracefully if slot not found
        
        return appointment


