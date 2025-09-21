from django import forms
from .models import CustomerFeedback

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


