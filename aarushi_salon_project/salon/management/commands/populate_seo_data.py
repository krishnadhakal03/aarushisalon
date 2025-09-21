from django.core.management.base import BaseCommand
from salon.models import SEOSettings, GoogleAnalytics, SEOPageContent

class Command(BaseCommand):
    help = 'Populate default SEO settings for the salon website'

    def handle(self, *args, **options):
        # Create default SEO settings for each page
        seo_data = {
            'home': {
                'page_title': 'Aarushi Salon - Best Hair Cut & Threading in Charlotte NC',
                'meta_description': 'Professional beauty salon in Charlotte NC. Best hair cut, threading, waxing, facial, makeup services. Book your appointment today!',
                'meta_keywords': 'salon in NC, best hair cut Charlotte, threading Charlotte, waxing Charlotte, facial Charlotte, makeup Charlotte, beauty salon NC, hair styling Charlotte',
                'h1_tag': 'Welcome to Aarushi Salon - Charlotte\'s Premier Beauty Destination',
                'h2_tag': 'Professional Beauty Services in Charlotte, North Carolina',
                'og_title': 'Aarushi Salon - Best Hair Cut & Threading in Charlotte NC',
                'og_description': 'Professional beauty salon in Charlotte NC. Best hair cut, threading, waxing, facial, makeup services. Book your appointment today!',
                'twitter_title': 'Aarushi Salon - Best Hair Cut & Threading in Charlotte NC',
                'twitter_description': 'Professional beauty salon in Charlotte NC. Best hair cut, threading, waxing, facial, makeup services.',
            },
            'about': {
                'page_title': 'About Aarushi Salon - Charlotte\'s Premier Beauty Destination',
                'meta_description': 'Learn about Aarushi Salon, Charlotte\'s premier beauty destination. Professional hair styling, threading, waxing, and skincare services.',
                'meta_keywords': 'about aarushi salon, charlotte beauty salon, professional hair styling, threading services, waxing services, skincare charlotte',
                'h1_tag': 'About Aarushi Salon',
                'h2_tag': 'Charlotte\'s Premier Beauty Destination',
            },
            'services': {
                'page_title': 'Beauty Services - Hair Cut, Threading, Waxing in Charlotte NC',
                'meta_description': 'Comprehensive beauty services at Aarushi Salon Charlotte. Hair styling, threading, waxing, facial, makeup, manicure, pedicure services.',
                'meta_keywords': 'beauty services charlotte, hair styling charlotte, threading charlotte, waxing charlotte, facial charlotte, makeup charlotte, manicure charlotte, pedicure charlotte',
                'h1_tag': 'Our Beauty Services',
                'h2_tag': 'Professional Beauty Treatments in Charlotte',
            },
            'gallery': {
                'page_title': 'Beauty Gallery - Aarushi Salon Charlotte Before & After Photos',
                'meta_description': 'View our beauty gallery showcasing amazing transformations. Hair styling, makeup, threading, and skincare results at Aarushi Salon Charlotte.',
                'meta_keywords': 'beauty gallery charlotte, hair styling gallery, makeup gallery, threading results, before after photos, salon gallery charlotte',
                'h1_tag': 'Beauty Gallery',
                'h2_tag': 'Amazing Transformations at Aarushi Salon',
            },
            'team': {
                'page_title': 'Meet Our Team - Professional Beauty Experts in Charlotte',
                'meta_description': 'Meet our talented team of beauty professionals at Aarushi Salon Charlotte. Experienced hair stylists, makeup artists, and skincare specialists.',
                'meta_keywords': 'beauty team charlotte, hair stylists charlotte, makeup artists charlotte, skincare specialists, beauty experts charlotte',
                'h1_tag': 'Meet Our Team',
                'h2_tag': 'Professional Beauty Experts',
            },
            'testimonials': {
                'page_title': 'Client Testimonials - Aarushi Salon Charlotte Reviews',
                'meta_description': 'Read client testimonials and reviews for Aarushi Salon Charlotte. See why we\'re the best beauty salon in North Carolina.',
                'meta_keywords': 'salon reviews charlotte, beauty salon testimonials, client reviews charlotte, aarushi salon reviews, best salon charlotte',
                'h1_tag': 'Client Testimonials',
                'h2_tag': 'What Our Clients Say',
            },
            'blog': {
                'page_title': 'Beauty Blog - Hair Care Tips & Beauty Advice from Aarushi Salon',
                'meta_description': 'Read our beauty blog for hair care tips, skincare advice, and beauty trends. Expert advice from Aarushi Salon Charlotte professionals.',
                'meta_keywords': 'beauty blog charlotte, hair care tips, skincare advice, beauty trends, salon blog, beauty tips charlotte',
                'h1_tag': 'Beauty Blog',
                'h2_tag': 'Expert Beauty Advice & Tips',
            },
            'contact': {
                'page_title': 'Contact Aarushi Salon - Book Appointment in Charlotte NC',
                'meta_description': 'Contact Aarushi Salon Charlotte to book your beauty appointment. Call us or visit our salon for hair styling, threading, waxing services.',
                'meta_keywords': 'contact aarushi salon, book appointment charlotte, salon contact charlotte, beauty appointment charlotte, salon phone charlotte',
                'h1_tag': 'Contact Us',
                'h2_tag': 'Book Your Beauty Appointment Today',
            },
            'pricing': {
                'page_title': 'Beauty Services Pricing - Aarushi Salon Charlotte Rates',
                'meta_description': 'View our competitive pricing for beauty services in Charlotte. Affordable hair styling, threading, waxing, facial, and makeup services.',
                'meta_keywords': 'beauty services pricing charlotte, salon rates charlotte, hair styling prices, threading prices, waxing prices charlotte',
                'h1_tag': 'Service Pricing',
                'h2_tag': 'Affordable Beauty Services in Charlotte',
            },
        }

        # Create SEO settings for each page
        for page_type, data in seo_data.items():
            seo_setting, created = SEOSettings.objects.get_or_create(
                page_type=page_type,
                defaults=data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created SEO settings for {page_type} page')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'SEO settings for {page_type} page already exist')
                )

        # Create default Google Analytics entry
        analytics, created = GoogleAnalytics.objects.get_or_create(
            id=1,
            defaults={
                'tracking_id': '',  # To be filled by admin
                'gtag_id': '',      # To be filled by admin
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created default Google Analytics entry')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Google Analytics entry already exists')
            )

        # Create some default SEO page content
        content_data = [
            {
                'page_type': 'home',
                'content_section': 'hero_text',
                'title': 'Welcome to Aarushi Salon',
                'content': 'Charlotte\'s premier beauty destination offering professional hair styling, threading, waxing, and skincare services.',
                'image_alt_text': 'Aarushi Salon Charlotte beauty services',
            },
            {
                'page_type': 'about',
                'content_section': 'intro_text',
                'title': 'About Our Salon',
                'content': 'Aarushi Salon has been serving the Charlotte community with exceptional beauty services for years. Our experienced team is dedicated to making you look and feel your best.',
                'image_alt_text': 'Aarushi Salon team and interior',
            },
        ]

        for content in content_data:
            seo_content, created = SEOPageContent.objects.get_or_create(
                page_type=content['page_type'],
                content_section=content['content_section'],
                defaults=content
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created SEO content for {content["page_type"]} - {content["content_section"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated SEO data!')
        )
