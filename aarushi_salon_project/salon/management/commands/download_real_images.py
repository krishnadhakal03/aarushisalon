from django.core.management.base import BaseCommand
from salon.models import GalleryImage
import os
import requests
from django.conf import settings
import time
import random

class Command(BaseCommand):
    help = 'Download real beauty service images from free sources'

    def download_image(self, url, filename):
        """Download image from URL and save to media directory"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Create gallery directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            self.stdout.write(f'Error downloading image: {str(e)}')
            return False

    def handle(self, *args, **options):
        # Real beauty service images from free sources
        # These are high-quality, royalty-free images from Unsplash, Pexels, etc.
        real_images = [
            # Skin Care Images
            {
                'title': 'Hydrating Facial Treatment',
                'description': 'Deep moisturizing facial for glowing, healthy skin',
                'category': 'Skin Care',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Anti-Aging Facial',
                'description': 'Advanced anti-aging treatment to reduce fine lines',
                'category': 'Skin Care',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Acne Treatment Facial',
                'description': 'Specialized treatment for acne-prone skin',
                'category': 'Skin Care',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=400&h=300&fit=crop&crop=face',
            },
            
            # Hair Styling Images
            {
                'title': 'Elegant Hair Styling',
                'description': 'Professional hair styling for any occasion',
                'category': 'Hair Styling',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Hair Cut & Blow Dry',
                'description': 'Fresh haircut with professional styling',
                'category': 'Hair Styling',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Hair Styling for Events',
                'description': 'Special occasion hair styling and updos',
                'category': 'Hair Styling',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=400&h=300&fit=crop&crop=face',
            },
            
            # Make Up Images
            {
                'title': 'Bridal Makeup',
                'description': 'Stunning bridal makeup for your special day',
                'category': 'Make Up',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Evening Makeup',
                'description': 'Glamorous evening makeup for special events',
                'category': 'Make Up',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Natural Day Makeup',
                'description': 'Fresh, natural makeup for everyday wear',
                'category': 'Make Up',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&h=300&fit=crop&crop=face',
            },
            
            # Waxing Images
            {
                'title': 'Full Body Waxing',
                'description': 'Complete hair removal for smooth, silky skin',
                'category': 'Waxing',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop',
            },
            {
                'title': 'Facial Waxing',
                'description': 'Precise facial hair removal and shaping',
                'category': 'Waxing',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Bikini Waxing',
                'description': 'Professional bikini area hair removal',
                'category': 'Waxing',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop',
            },
            
            # Massage Images
            {
                'title': 'Relaxing Body Massage',
                'description': 'Therapeutic massage for stress relief and relaxation',
                'category': 'Massage',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400&h=300&fit=crop',
            },
            {
                'title': 'Deep Tissue Massage',
                'description': 'Intensive massage for muscle tension relief',
                'category': 'Massage',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop',
            },
            {
                'title': 'Aromatherapy Massage',
                'description': 'Healing massage with essential oils',
                'category': 'Massage',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400&h=300&fit=crop',
            },
            
            # Threading Images
            {
                'title': 'Eyebrow Threading',
                'description': 'Precise eyebrow shaping and hair removal',
                'category': 'Threading',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Facial Threading',
                'description': 'Complete facial hair removal and shaping',
                'category': 'Threading',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=400&h=300&fit=crop&crop=face',
            },
            
            # Color Images
            {
                'title': 'Hair Coloring',
                'description': 'Professional hair coloring and highlights',
                'category': 'Color',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Balayage Highlights',
                'description': 'Natural-looking hair highlights and color',
                'category': 'Color',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop&crop=face',
            },
            
            # Bridal Package Images
            {
                'title': 'Complete Bridal Package',
                'description': 'Full bridal beauty package for your special day',
                'category': 'Bridal Package',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=300&fit=crop&crop=face',
            },
            {
                'title': 'Bridal Hair & Makeup',
                'description': 'Stunning bridal hair styling and makeup',
                'category': 'Bridal Package',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=400&h=300&fit=crop&crop=face',
            },
            
            # Manicure Images
            {
                'title': 'Gel Manicure',
                'description': 'Long-lasting gel nail polish application',
                'category': 'Manicure',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=300&fit=crop',
            },
            {
                'title': 'Nail Art Design',
                'description': 'Creative nail art and design services',
                'category': 'Manicure',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=300&fit=crop',
            },
            
            # Pedicure Images
            {
                'title': 'Spa Pedicure',
                'description': 'Relaxing foot care and nail treatment',
                'category': 'Pedicure',
                'is_featured': True,
                'url': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=300&fit=crop',
            },
            {
                'title': 'French Pedicure',
                'description': 'Classic French pedicure with white tips',
                'category': 'Pedicure',
                'is_featured': False,
                'url': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=300&fit=crop',
            },
        ]

        # Clear existing gallery images
        GalleryImage.objects.all().delete()
        self.stdout.write('Cleared existing gallery images.')

        # Download and create gallery images
        for i, data in enumerate(real_images, 1):
            # Create the gallery image record first
            gallery_image = GalleryImage.objects.create(
                title=data['title'],
                description=data['description'],
                is_featured=data['is_featured'],
                is_active=True
            )
            
            # Download the real image
            dest_path = os.path.join(settings.MEDIA_ROOT, 'gallery', f'gallery_{gallery_image.id}.jpg')
            
            if self.download_image(data['url'], dest_path):
                # Update the gallery image with the downloaded image
                gallery_image.image = f'gallery/gallery_{gallery_image.id}.jpg'
                gallery_image.save()
                self.stdout.write(f'Downloaded real image: {data["title"]} ({data["category"]})')
            else:
                # If download fails, create a simple placeholder
                self.stdout.write(f'Failed to download {data["title"]}, creating placeholder...')
                # Keep the gallery image record but without image
                gallery_image.save()
            
            # Add a small delay to be respectful to the image servers
            time.sleep(0.5)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(real_images)} real beauty service images!')
        )
