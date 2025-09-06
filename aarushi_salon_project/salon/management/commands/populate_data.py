from django.core.management.base import BaseCommand
from salon.models import (
    ServiceCategory, Service, TeamMember, Testimonial, 
    GalleryImage, BlogPost, ContactInfo, SiteContent
)


class Command(BaseCommand):
    help = 'Populate the database with Aarushi Salon content'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate database...')

        # Create Contact Information
        contact_info, created = ContactInfo.objects.get_or_create(
            defaults={
                'phone': '+123456789',
                'email': 'info@aarushisalon.com',
                'address': '123 Street, New York, USA',
                'facebook_url': 'https://facebook.com/aarushisalon',
                'instagram_url': 'https://instagram.com/aarushisalon',
                'linkedin_url': 'https://linkedin.com/company/aarushisalon',
                'twitter_url': 'https://twitter.com/aarushisalon',
            }
        )
        if created:
            self.stdout.write('Created contact information')

        # Create Site Content
        site_content_data = [
            ('hero_title', 'Welcome', 'Welcome to Aarushi Salon'),
            ('hero_subtitle', 'Best Beauty Service', 'Best Beauty Service'),
            ('about_title', 'About Us', 'About Us'),
            ('about_subtitle', 'Why People Choose Us!', 'Why People Choose Us!'),
            ('about_content', 'About Content', 'With over ten years experience in the industry, our certified therapists are dedicated to providing you with the highest level of service, with each treatment and package fully customized and tailored to your personal needs.'),
            ('experience_years', '10', '10'),
            ('happy_customers', '999', '999'),
        ]

        for content_type, title, content in site_content_data:
            SiteContent.objects.get_or_create(
                content_type=content_type,
                defaults={'title': title, 'content': content}
            )
        self.stdout.write('Created site content')

        # Create Service Categories
        categories_data = [
            ('Skin Care', 'Professional skin care treatments for all skin types', 'fas fa-spa'),
            ('Waxing', 'Hair removal services using premium waxing techniques', 'fas fa-cut'),
            ('Threading', 'Precise hair removal using traditional threading method', 'fas fa-eye'),
            ('Hair Styling', 'Professional hair cutting, styling, and coloring services', 'fas fa-cut'),
            ('Color', 'Hair coloring and highlighting services', 'fas fa-palette'),
            ('Herbal Bleach', 'Natural herbal skin lightening treatments', 'fas fa-leaf'),
            ('Body Scrub', 'Exfoliating body treatments for smooth, healthy skin', 'fas fa-hand-holding-heart'),
            ('Henna Design', 'Beautiful henna art for special occasions', 'fas fa-paint-brush'),
            ('Make Up', 'Professional makeup services for all occasions', 'fas fa-makeup'),
            ('Bridal Package', 'Complete bridal beauty packages', 'fas fa-heart'),
            ('Massage', 'Relaxing and therapeutic massage services', 'fas fa-hands'),
        ]

        for name, description, icon in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=name,
                defaults={'description': description, 'icon': icon}
            )
            if created:
                self.stdout.write(f'Created category: {name}')

        # Create Services based on Aarushi Salon website content
        services_data = [
            # Skin Care Services
            ('Skin Care', 'Express Facial', 'This express facial is ideal for those on the go. Your skin is cleansed, lightly exfoliated and gently massaged. A pore-refining mask is then applied, followed by a veil of light moisturiser.', 45.00, True),
            ('Skin Care', 'Organic Facial', 'The right care is very essential for your face to keep it youthful, healthy and fresh. Organic facial is the perfect blend of natural products to keep you fresh and clean.', 65.00, True),
            ('Skin Care', 'Acne Treatment', 'If you are struggling with acne, your typical acne facial cleanser might not be cutting it. The acne facial is an alternative treatment designed to treat the root cause of acne with minimal side effects.', 65.00, True),
            ('Skin Care', 'Anti Aging', 'Fine-lines, wrinkles, pigmentation and loss of skin tone are all associated with skin aging. With professional skin care treatments you can prevent the signs of aging.', 65.00, True),
            ('Skin Care', 'Vitamin-C', 'An anti-toxidant, anti-aging mask designed to rejuvenate the skin by stimulating collagen synthesis, replicating elastin and protecting against free radicals.', 65.00, True),
            
            # Waxing Services
            ('Waxing', 'Full Arm', 'Remove unwanted hair from full arms by applying wax and then peeling off the wax and hairs together.', 40.00, False),
            ('Waxing', 'Half Arm', 'Remove unwanted hair from half arms by applying wax and then peeling off the wax and hairs together.', 30.00, False),
            ('Waxing', 'Under Arms', 'Remove unwanted hair from under arms by applying wax and then peeling off the wax and hairs together.', 20.00, False),
            ('Waxing', 'Full Legs', 'Remove unwanted hair from full legs by applying wax and then peeling off the wax and hairs together.', 60.00, False),
            ('Waxing', 'Half Legs', 'Remove unwanted hair from half legs by applying wax and then peeling off the wax and hairs together.', 40.00, False),
            ('Waxing', 'Bikini', 'Remove unwanted hair from bikini area by applying wax and then peeling off the wax and hairs together.', 35.00, False),
            ('Waxing', 'Brazilian', 'Remove unwanted hair from Brazilian area by applying wax and then peeling off the wax and hairs together.', 60.00, False),
            ('Waxing', 'Back', 'Remove unwanted hair from back by applying wax and then peeling off the wax and hairs together.', 40.00, False),
            ('Waxing', 'Chest', 'Remove unwanted hair from chest by applying wax and then peeling off the wax and hairs together.', 35.00, False),
            ('Waxing', 'Stomach', 'Remove unwanted hair from stomach by applying wax and then peeling off the wax and hairs together.', 35.00, False),
            ('Waxing', 'Full Body', 'Remove unwanted hair from full body by applying wax and then peeling off the wax and hairs together.', 200.00, True),
            
            # Threading Services
            ('Threading', 'Eyebrows Threading', 'A pro treatment that shapes and defines your eyebrows whilst making the most of your natural beauty- alternative to waxing', 12.00, False),
            ('Threading', 'Upper Lips Threading', 'Precise hair removal from upper lip area using traditional threading method', 8.00, False),
            ('Threading', 'Forehead Threading', 'Hair removal from forehead area using threading technique', 12.00, False),
            ('Threading', 'Chin Threading', 'Hair removal from chin area using threading technique', 12.00, False),
            ('Threading', 'Neck Threading', 'Hair removal from neck area using threading technique', 12.00, False),
            ('Threading', 'Side Burns Threading', 'Threading of sideburns is similar like you get your eyebrows done. Threading helps to pull out the hair from the roots.', 12.00, False),
            ('Threading', 'Full Face Threading', 'Includes whole face threading. Hair grows back finer than before.', 45.00, True),
            
            # Hair Styling Services
            ('Hair Styling', 'Men Haircut', 'Professional haircut services for men', 30.00, False),
            ('Hair Styling', 'Ladies Haircut', 'Professional haircut services for women', 35.00, False),
            ('Hair Styling', 'Kid\'s Haircut', 'Professional haircut services for children', 30.00, False),
            ('Hair Styling', 'Shampoo & Blow Dry', 'Professional shampoo and blow dry service', 50.00, False),
            ('Hair Styling', 'Shampoo, Cut & Style', 'Complete hair service including shampoo, cut and styling', 60.00, False),
            ('Hair Styling', 'Flat Iron', 'Professional flat iron styling service', 40.00, False),
            ('Hair Styling', 'Curls', 'Professional curling service', 40.00, False),
            ('Hair Styling', 'Hair Do\'s', 'Professional hair styling for special occasions', 50.00, False),
            ('Hair Styling', 'Deep Conditioning', 'Intensive hair conditioning treatment', 30.00, False),
            ('Hair Styling', 'Perm', 'Professional hair perming service', 130.00, False),
            ('Hair Styling', 'Dominican Blowout', 'Professional Dominican blowout service', 40.00, False),
            ('Hair Styling', 'Keratin Treatment', 'Professional keratin treatment for smooth, manageable hair', 200.00, True),
            
            # Color Services
            ('Color', 'Brow Tint', 'Professional eyebrow tinting service', 20.00, False),
            ('Color', 'Lash Tint', 'Professional eyelash tinting service', 25.00, False),
            ('Color', 'Hair Color', 'Professional hair coloring service', 50.00, False),
            ('Color', 'Henna', 'Natural henna hair coloring service', 50.00, False),
            ('Color', 'Full Highlights', 'Complete hair highlighting service', 180.00, True),
            ('Color', 'Per Foil', 'Individual foil highlighting service', 15.00, False),
            ('Color', 'Partial Highlights', 'Partial hair highlighting service', 120.00, False),
            ('Color', 'Men\'s Hair Color', 'Professional hair coloring service for men', 50.00, False),
            
            # Herbal Bleach Services
            ('Herbal Bleach', 'Face', 'All natural ingredients & cosmetics. Complete Herbal skin lightening treatment for face', 25.00, False),
            ('Herbal Bleach', 'Back', 'All natural ingredients & cosmetics. Complete Herbal skin lightening treatment for back', 35.00, False),
            ('Herbal Bleach', 'Full Body', 'All natural ingredients & cosmetics. Complete Herbal skin lightening treatment for full body', 125.00, True),
            
            # Body Scrub Services
            ('Body Scrub', 'Back', 'Popular way to stimulate skin circulation and get rid of dry, dead skin cells on back', 35.00, False),
            ('Body Scrub', 'Half Body', 'Popular way to stimulate skin circulation and get rid of dry, dead skin cells on half body', 60.00, False),
            ('Body Scrub', 'Full Body', 'Popular way to stimulate skin circulation and get rid of dry, dead skin cells on full body', 115.00, True),
            
            # Henna Design Services
            ('Henna Design', 'Hand', 'Henna is an important part in Indian culture, for all the ladies and girls out there, best designs for hands suited for any event', 20.00, False),
            ('Henna Design', 'Bridal', 'Expose your bridal charm! Complete bridal henna design package', 150.00, True),
            
            # Make Up Services
            ('Make Up', 'Hair & Make Up', 'Complete hair and makeup service for special occasions', 150.00, True),
            ('Make Up', 'Bridal Make Up', 'Professional bridal makeup service', 150.00, True),
            ('Make Up', 'Bridal Hair', 'Professional bridal hair styling service', 150.00, True),
            
            # Bridal Package Services
            ('Bridal Package', 'Hair + Make Up', 'Perfect bridal packages to make the most important day of your life even more fabulous!', 300.00, True),
            
            # Massage Services
            ('Massage', 'Head Massage', 'Deep tissue massage to release chronic muscle tension in head and neck area', 25.00, False),
            ('Massage', 'Back Massage', 'Deep tissue massage to release chronic muscle tension in back area', 40.00, False),
            ('Massage', 'Hour Massage', 'One hour deep tissue massage to release chronic muscle tension', 70.00, True),
            ('Massage', 'Aroma Therapy', 'Aromatherapy massage with essential oils for relaxation and wellness', 75.00, True),
        ]

        for category_name, service_name, description, price, is_featured in services_data:
            try:
                category = ServiceCategory.objects.get(name=category_name)
                service, created = Service.objects.get_or_create(
                    category=category,
                    name=service_name,
                    defaults={
                        'description': description,
                        'price': price,
                        'is_featured': is_featured,
                    }
                )
                if created:
                    self.stdout.write(f'Created service: {service_name}')
            except ServiceCategory.DoesNotExist:
                self.stdout.write(f'Category not found: {category_name}')

        # Create Team Members
        team_members_data = [
            ('Lily Taylor', 'Hair Specialist', 'Expert hair stylist with over 8 years of experience in cutting, coloring, and styling. Specializes in modern and classic looks.', 'https://facebook.com/lilytaylor', 'https://instagram.com/lilytaylor', 'https://linkedin.com/in/lilytaylor'),
            ('Olivia Smith', 'Nail Designer', 'Professional nail artist specializing in manicures, pedicures, and nail art. Known for attention to detail and creative designs.', 'https://facebook.com/oliviasmith', 'https://instagram.com/oliviasmith', 'https://linkedin.com/in/oliviasmith'),
            ('Ava Brown', 'Beauty Specialist', 'Certified beauty specialist with expertise in skincare, facials, and makeup. Passionate about helping clients achieve their beauty goals.', 'https://facebook.com/avabrown', 'https://instagram.com/avabrown', 'https://linkedin.com/in/avabrown'),
            ('Amelia Jones', 'Spa Specialist', 'Experienced spa specialist providing relaxing massage and wellness treatments. Certified in various massage techniques and aromatherapy.', 'https://facebook.com/ameliajones', 'https://instagram.com/ameliajones', 'https://linkedin.com/in/ameliajones'),
        ]

        for name, position, bio, facebook, instagram, linkedin in team_members_data:
            TeamMember.objects.get_or_create(
                name=name,
                defaults={
                    'position': position,
                    'bio': bio,
                    'facebook_url': facebook,
                    'instagram_url': instagram,
                    'linkedin_url': linkedin,
                }
            )
        self.stdout.write('Created team members')

        # Create Testimonials
        testimonials_data = [
            ('Jenita M.', 'Regular Customer', 'Convenient salon located in a shopping district near Walmart. I\'ve been coming here for a year to get my eyebrow threaded. Quick and quite painless here. Always satisfied with the look and the owner always give me an eyebrow massage with oil when she finishes. It helps with the redness for sure. Never quick or cut corners to get it over. Even precise with trimming and plucking where needed. I walk in and pretty much never have to wait.', 5, True),
            ('Stacey H.', 'Satisfied Customer', 'Super friendly place! I walked in on a whim to see what services they offer. Pretty much everything! I tried out the eyebrow wax first. Great job with that. She also introduced me to threading for the first time. Very interesting and didn\'t hurt like I expected it to. While I was there I decided to get a deep hair conditioning treatment. That felt amazing. I\'m definitely looking forward to trying out their facials next month.', 5, True),
            ('Ruchi M.', 'Happy Client', 'Made an appointment for eyebrows based on the great reviews my friends gave. Anjana is great at shaping eyebrows. She took her time and didn\'t rush at all. Highly recommend this place if you want perfectly shaped brows.', 5, True),
            ('Carmel Woodard', 'Loyal Customer', 'Great services, amazing work, and super friendly staff. I will recommend this place to any and everyone!', 5, True),
        ]

        for client_name, profession, content, rating, is_featured in testimonials_data:
            Testimonial.objects.get_or_create(
                client_name=client_name,
                defaults={
                    'profession': profession,
                    'content': content,
                    'rating': rating,
                    'is_featured': is_featured,
                }
            )
        self.stdout.write('Created testimonials')

        # Create Blog Posts
        blog_posts_data = [
            ('How to Extend The Life of Your Haircolor', 'how-to-extend-the-life-of-your-haircolor', 'Learn professional tips and tricks to make your hair color last longer and maintain its vibrancy between salon visits.', 'Hair color maintenance is essential for keeping your color looking fresh and vibrant. Here are some expert tips to extend the life of your haircolor...', 'Hair Salon', True),
            ('Hottest Hairstyles and Haircuts in 2024', 'hottest-hairstyles-and-haircuts-in-2024', 'Discover the latest hair trends and most popular hairstyles that are taking the beauty world by storm this year.', 'From bold cuts to elegant styles, 2024 brings exciting new hair trends. Here are the hottest hairstyles and haircuts that are trending right now...', 'Hair Salon', True),
        ]

        for title, slug, excerpt, content, category, is_featured in blog_posts_data:
            BlogPost.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'excerpt': excerpt,
                    'content': content,
                    'category': category,
                    'is_featured': is_featured,
                }
            )
        self.stdout.write('Created blog posts')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with Aarushi Salon content!')
        )
