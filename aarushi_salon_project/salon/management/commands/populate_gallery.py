from django.core.management.base import BaseCommand
from salon.models import GalleryImage, ServiceCategory
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import random

class Command(BaseCommand):
    help = 'Populate gallery with AI-generated category-specific images'

    def create_ai_image(self, category_name, service_type, width=400, height=300):
        """Create AI-generated placeholder images for different service categories"""
        # Create a new image with a gradient background
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Define color schemes for different categories
        color_schemes = {
            'Skin Care': [(255, 192, 203), (255, 228, 225), (255, 182, 193)],  # Pink tones
            'Hair Styling': [(139, 90, 60), (160, 82, 45), (210, 180, 140)],  # Brown tones
            'Make Up': [(255, 20, 147), (255, 105, 180), (255, 192, 203)],    # Pink/Magenta
            'Waxing': [(255, 228, 196), (255, 218, 185), (255, 222, 173)],    # Cream tones
            'Massage': [(144, 238, 144), (152, 251, 152), (173, 255, 173)],   # Green tones
            'Threading': [(255, 228, 225), (255, 240, 245), (255, 250, 250)], # Light pink
            'Color': [(255, 165, 0), (255, 140, 0), (255, 215, 0)],          # Orange/Gold
            'Bridal Package': [(255, 192, 203), (255, 228, 225), (255, 240, 245)], # Pink/White
            'Manicure': [(255, 20, 147), (255, 105, 180), (255, 192, 203)],   # Pink
            'Pedicure': [(255, 20, 147), (255, 105, 180), (255, 192, 203)],   # Pink
        }
        
        # Get color scheme for the category
        colors = color_schemes.get(category_name, [(139, 90, 60), (166, 124, 82), (210, 180, 140)])
        
        # Create gradient background
        for y in range(height):
            color_ratio = y / height
            r = int(colors[0][0] * (1 - color_ratio) + colors[1][0] * color_ratio)
            g = int(colors[0][1] * (1 - color_ratio) + colors[1][1] * color_ratio)
            b = int(colors[0][2] * (1 - color_ratio) + colors[1][2] * color_ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add decorative elements based on service type
        if 'Hair' in service_type:
            # Draw hair-like curves
            for i in range(5):
                x = random.randint(50, width-50)
                y = random.randint(50, height-50)
                draw.ellipse([x-20, y-20, x+20, y+20], outline=colors[2], width=3)
        elif 'Make' in service_type or 'Bridal' in service_type:
            # Draw makeup-like elements
            for i in range(8):
                x = random.randint(30, width-30)
                y = random.randint(30, height-30)
                draw.ellipse([x-10, y-10, x+10, y+10], fill=colors[1])
        elif 'Skin' in service_type:
            # Draw skin care elements
            for i in range(6):
                x = random.randint(40, width-40)
                y = random.randint(40, height-40)
                draw.ellipse([x-15, y-15, x+15, y+15], outline=colors[0], width=2)
        elif 'Massage' in service_type:
            # Draw massage elements
            for i in range(4):
                x = random.randint(60, width-60)
                y = random.randint(60, height-60)
                draw.ellipse([x-25, y-25, x+25, y+25], outline=colors[1], width=4)
        elif 'Nail' in service_type or 'Manicure' in service_type or 'Pedicure' in service_type:
            # Draw nail art elements
            for i in range(10):
                x = random.randint(20, width-20)
                y = random.randint(20, height-20)
                draw.ellipse([x-8, y-8, x+8, y+8], fill=colors[2])
        
        # Add category name
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw category name
        text = category_name
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Add text shadow
        draw.text((x+2, y+2), text, fill=(0, 0, 0, 128), font=font)
        # Add main text
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        return img

    def handle(self, *args, **options):
        # Get all service categories
        categories = ServiceCategory.objects.filter(is_active=True)
        
        # Sample gallery data with category-specific content
        gallery_data = [
            # Skin Care Category
            {
                'title': 'Hydrating Facial Treatment',
                'description': 'Deep moisturizing facial for glowing, healthy skin',
                'category': 'Skin Care',
                'is_featured': True,
            },
            {
                'title': 'Anti-Aging Facial',
                'description': 'Advanced anti-aging treatment to reduce fine lines',
                'category': 'Skin Care',
                'is_featured': False,
            },
            {
                'title': 'Acne Treatment Facial',
                'description': 'Specialized treatment for acne-prone skin',
                'category': 'Skin Care',
                'is_featured': False,
            },
            
            # Hair Styling Category
            {
                'title': 'Elegant Hair Styling',
                'description': 'Professional hair styling for any occasion',
                'category': 'Hair Styling',
                'is_featured': True,
            },
            {
                'title': 'Hair Cut & Blow Dry',
                'description': 'Fresh haircut with professional styling',
                'category': 'Hair Styling',
                'is_featured': False,
            },
            {
                'title': 'Hair Styling for Events',
                'description': 'Special occasion hair styling and updos',
                'category': 'Hair Styling',
                'is_featured': False,
            },
            
            # Make Up Category
            {
                'title': 'Bridal Makeup',
                'description': 'Stunning bridal makeup for your special day',
                'category': 'Make Up',
                'is_featured': True,
            },
            {
                'title': 'Evening Makeup',
                'description': 'Glamorous evening makeup for special events',
                'category': 'Make Up',
                'is_featured': False,
            },
            {
                'title': 'Natural Day Makeup',
                'description': 'Fresh, natural makeup for everyday wear',
                'category': 'Make Up',
                'is_featured': False,
            },
            
            # Waxing Category
            {
                'title': 'Full Body Waxing',
                'description': 'Complete hair removal for smooth, silky skin',
                'category': 'Waxing',
                'is_featured': True,
            },
            {
                'title': 'Facial Waxing',
                'description': 'Precise facial hair removal and shaping',
                'category': 'Waxing',
                'is_featured': False,
            },
            {
                'title': 'Bikini Waxing',
                'description': 'Professional bikini area hair removal',
                'category': 'Waxing',
                'is_featured': False,
            },
            
            # Massage Category
            {
                'title': 'Relaxing Body Massage',
                'description': 'Therapeutic massage for stress relief and relaxation',
                'category': 'Massage',
                'is_featured': True,
            },
            {
                'title': 'Deep Tissue Massage',
                'description': 'Intensive massage for muscle tension relief',
                'category': 'Massage',
                'is_featured': False,
            },
            {
                'title': 'Aromatherapy Massage',
                'description': 'Healing massage with essential oils',
                'category': 'Massage',
                'is_featured': False,
            },
            
            # Threading Category
            {
                'title': 'Eyebrow Threading',
                'description': 'Precise eyebrow shaping and hair removal',
                'category': 'Threading',
                'is_featured': True,
            },
            {
                'title': 'Facial Threading',
                'description': 'Complete facial hair removal and shaping',
                'category': 'Threading',
                'is_featured': False,
            },
            
            # Color Category
            {
                'title': 'Hair Coloring',
                'description': 'Professional hair coloring and highlights',
                'category': 'Color',
                'is_featured': True,
            },
            {
                'title': 'Balayage Highlights',
                'description': 'Natural-looking hair highlights and color',
                'category': 'Color',
                'is_featured': False,
            },
            
            # Bridal Package Category
            {
                'title': 'Complete Bridal Package',
                'description': 'Full bridal beauty package for your special day',
                'category': 'Bridal Package',
                'is_featured': True,
            },
            {
                'title': 'Bridal Hair & Makeup',
                'description': 'Stunning bridal hair styling and makeup',
                'category': 'Bridal Package',
                'is_featured': False,
            },
            
            # Manicure Category
            {
                'title': 'Gel Manicure',
                'description': 'Long-lasting gel nail polish application',
                'category': 'Manicure',
                'is_featured': True,
            },
            {
                'title': 'Nail Art Design',
                'description': 'Creative nail art and design services',
                'category': 'Manicure',
                'is_featured': False,
            },
            
            # Pedicure Category
            {
                'title': 'Spa Pedicure',
                'description': 'Relaxing foot care and nail treatment',
                'category': 'Pedicure',
                'is_featured': True,
            },
            {
                'title': 'French Pedicure',
                'description': 'Classic French pedicure with white tips',
                'category': 'Pedicure',
                'is_featured': False,
            },
        ]

        # Clear existing gallery images
        GalleryImage.objects.all().delete()
        self.stdout.write('Cleared existing gallery images.')

        # Create gallery images
        for data in gallery_data:
            # Create the gallery image record first
            gallery_image = GalleryImage.objects.create(
                title=data['title'],
                description=data['description'],
                is_featured=data['is_featured'],
                is_active=True
            )
            
            # Generate AI image for this category
            try:
                ai_image = self.create_ai_image(data['category'], data['title'])
                
                # Save the AI-generated image
                dest_path = os.path.join(settings.MEDIA_ROOT, 'gallery', f'gallery_{gallery_image.id}.jpg')
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                ai_image.save(dest_path, 'JPEG', quality=95)
                
                # Update the gallery image with the generated image
                gallery_image.image = f'gallery/gallery_{gallery_image.id}.jpg'
                gallery_image.save()
                
                self.stdout.write(f'Created AI gallery image: {data["title"]} ({data["category"]})')
                
            except Exception as e:
                self.stdout.write(f'Error creating AI image for {data["title"]}: {str(e)}')
                # Fallback to existing static image
                try:
                    import shutil
                    source_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'img', 'gallery-1.jpg')
                    dest_path = os.path.join(settings.MEDIA_ROOT, 'gallery', f'gallery_{gallery_image.id}.jpg')
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    if os.path.exists(source_path):
                        shutil.copy2(source_path, dest_path)
                        gallery_image.image = f'gallery/gallery_{gallery_image.id}.jpg'
                        gallery_image.save()
                        self.stdout.write(f'Created fallback gallery image: {data["title"]}')
                except Exception as e2:
                    self.stdout.write(f'Error with fallback image for {data["title"]}: {str(e2)}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(gallery_data)} AI-generated gallery images!')
        )
