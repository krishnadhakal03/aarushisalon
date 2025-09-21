from django.core.management.base import BaseCommand
from salon.models import Testimonial

class Command(BaseCommand):
    help = 'Add sample feedback/testimonials to the database'

    def handle(self, *args, **options):
        # Clear existing testimonials
        Testimonial.objects.all().delete()
        
        # Sample testimonials
        testimonials_data = [
            {
                'client_name': 'Sarah Johnson',
                'client_profession': 'Hair Styling & Color',
                'content': 'Absolutely amazing experience! The staff was professional and my hair looks better than ever. The color is exactly what I wanted and the cut is perfect. I will definitely be coming back!',
                'rating': 5,
                'is_active': True,
                'is_featured': True
            },
            {
                'client_name': 'Maria Rodriguez',
                'client_profession': 'Facial Treatment',
                'content': 'The facial treatment was incredibly relaxing and my skin feels so smooth and refreshed. The esthetician was very knowledgeable and made me feel comfortable throughout the entire process.',
                'rating': 5,
                'is_active': True,
                'is_featured': True
            },
            {
                'client_name': 'Jennifer Chen',
                'client_profession': 'Eyebrow Threading',
                'content': 'Best eyebrow threading I have ever had! The technician was very precise and gentle. My eyebrows look perfect and the service was quick and efficient. Highly recommend!',
                'rating': 5,
                'is_active': True,
                'is_featured': True
            },
            {
                'client_name': 'Lisa Thompson',
                'client_profession': 'Manicure & Pedicure',
                'content': 'The manicure and pedicure service was top-notch. The nail technician was very detail-oriented and my nails look beautiful. The salon is clean and the atmosphere is very relaxing.',
                'rating': 4,
                'is_active': True,
                'is_featured': True
            },
            {
                'client_name': 'Anonymous',
                'client_profession': 'Bridal Package',
                'content': 'I had my bridal package done here and I could not be happier! The team made me feel like a princess on my special day. Everything was perfect from hair to makeup to nails.',
                'rating': 5,
                'is_active': True,
                'is_featured': True
            }
        ]
        
        # Create testimonials
        for data in testimonials_data:
            Testimonial.objects.create(**data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(testimonials_data)} sample testimonials!')
        )


