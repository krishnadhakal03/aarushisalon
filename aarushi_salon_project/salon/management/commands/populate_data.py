from django.core.management.base import BaseCommand
from salon.models import (
    ServiceCategory, Service, TeamMember, Testimonial, 
    GalleryImage, BlogPost, ContactInfo, SiteContent,
    ThemeSettings, SiteImages, ServiceIcons, SiteSettings
)


class Command(BaseCommand):
    help = 'Populate the database with Aarushi Salon content'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate database...')

        # Create Contact Information (Based on Aarushi Salon website)
        contact_info, created = ContactInfo.objects.get_or_create(
            defaults={
                'phone': '+1 (555) 123-4567',  # Update with actual phone from website
                'email': 'info@arushisalon.com',
                'address': 'Convenient salon located in a shopping district near Walmart',
                'facebook_url': 'https://facebook.com/arushisalon',
                'instagram_url': 'https://instagram.com/arushisalon',
                'linkedin_url': 'https://linkedin.com/company/arushisalon',
                'twitter_url': 'https://twitter.com/arushisalon',
            }
        )
        if created:
            self.stdout.write('Created contact information')

        # Create Site Content (Based on Aarushi Salon website)
        site_content_data = [
            ('hero_title', 'Aarushi Salon', 'Aarushi Salon'),
            ('hero_subtitle', 'Best Beauty Service', 'Best Beauty Service'),
            ('about_title', 'About Us', 'About Us'),
            ('about_subtitle', 'Why People Choose Us!', 'Why People Choose Us!'),
            ('about_content', 'About Content', 'With over ten years experience in the industry, our certified therapists are dedicated to providing you with the highest level of service, with each treatment and package fully customized and tailored to your personal needs.'),
            ('experience_years', '10', '10'),
            ('happy_customers', '500+', '500+'),
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
            ('Waxing', 'Remove unwanted hair from (a part of the body) by applying wax and then peeling off the wax and hairs together.', 'fas fa-hand-holding-heart'),
            ('Massage', 'Deep tissue massage to release chronic muscle tension. Manual manipulation of soft body tissues (muscle, connective tissue, tendons and ligaments) to enhance a person\'s health and well-being.', 'fas fa-hands'),
            ('Threading', 'As opposed to waxing, tweezing, or lasers, threading is considered one of the safest and most precise methods of hair removal, especially in the delicate areas surrounding the eye. "Threading allows our specialists to have greater control over which hairs are removed,"', 'fas fa-eye'),
            ('Hair Styling', 'Something Special! Treat yourself, boost confidence & relax. Create any look for any type of hair with professional styling at Aarushi Salon.', 'fas fa-cut'),
            ('Color', 'Add style to your busy life, create one cohesive and natural look with coloring at Aarushi Salon. Book Appointment or Call us to ask for more details!', 'fas fa-palette'),
            ('Herbal Bleach', 'All natural ingredients & cosmetics. Complete Herbal skin lightening treatment; Unique herbal ingredients are soothing to the skin; Enriched with herbal extracts of vegetables, fruits, flowers & Herbs from Himalayas at Aarushi Salon!', 'fas fa-leaf'),
            ('Body Scrub', 'Popular way to stimulate skin circulation and get rid of dry, dead skin cells. Firm, smooth and detoxify your whole body with an exfoliating body scrub at Aarushi Salon.', 'fas fa-hand-holding-heart'),
            ('Henna Design', 'Henna is an important part in Indian culture, for all the ladies and girls out there, best designs for hands suited for any even. Expose your bridal charm!', 'fas fa-paint-brush'),
            ('Make Up', 'Gentle ingredients promote healthy skin , Versatile pigments wet or dry as a temporary hair colorant, lip color, blush, highlighter, eye shadow, eyeliner, and body shimmer. Beautify your confidence!', 'fas fa-paint-brush'),
            ('Bridal Package', 'Perfect bridal packages to make the most important day of your life even more fabulous!', 'fas fa-heart'),
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

        # Create Testimonials (Real reviews from Aarushi Salon website)
        testimonials_data = [
            ('Jenita M.', 'Yelp Review', 'Convenient salon located in a shopping district near Walmart. I\'ve been coming here for a year to get my eyebrow threaded. Quick and quite painless here. Always satisfied with the look and the owner always give me an eyebrow massage with oil when she finishes. It helps with the redness for sure. Never quick or cut corners to get it over. Even precise with trimming and plucking where needed. I walk in and pretty much never have to wait. Canned soft drinks and water available. Cash and debit/credit accepted. You may can find a coupon for first time customer next door at Kona Snow for eyebrow, hair, and massages.', 5, True),
            ('Stacey H.', 'Yelp Review', 'Super friendly place! I walked in on a whim to see what services they offer. Pretty much everything! I tried out the eyebrow wax first. Great job with that. She also introduced me to threading for the first time. Very interesting and didn\'t hurt like I expected it to. While I was there I decided to get a deep hair conditioning treatment. That felt amazing. I\'m definitely looking forward to trying out their facials next month. Update: I decided to get a cut and color done yesterday. Amazing! I had the best style done. She\'s wonderful! I\'m very picky about my blow out. I don\'t ever want to wash it again! My hair is naturally curly so I\'m loving this!!', 5, True),
            ('Ruchi M.', 'Yelp Review', 'Made an appointment for eyebrows based on the great reviews my friends gave. Anjana is great at shaping eyebrows. She took her time and didn\'t rush at all. Highly recommend this place if you want perfectly shaped brows.', 5, True),
            ('Carmel Woodard', 'Google Review', 'Great services, amazing work, and super friendly staff. I will recommend this place to any and everyone!', 5, True),
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
            ('Best Hair Styles for 2024', 'best-hair-styles-2024', 'Discover the most trending and flattering hair styles that will make you look stunning this year.', 'Hair styling is an art form that evolves with each season. In 2024, we\'re seeing a beautiful blend of classic elegance and modern edge. From the timeless bob with a contemporary twist to the romantic long layers that frame your face perfectly, there\'s a style for every personality and face shape. Our expert stylists have curated the most flattering cuts that work for both professional settings and special occasions. Whether you prefer short, medium, or long hair, we\'ll help you find the perfect style that enhances your natural beauty and boosts your confidence. The key is choosing a cut that complements your face shape, hair texture, and lifestyle. Don\'t be afraid to experiment with layers, bangs, or color highlights to make your look truly unique.', 'Hair Styling', 'published', 'hair, styling, trends, 2024, cuts, beauty', True),
            ('Facial Treatments: Your Complete Guide', 'facial-treatments-guide', 'Everything you need to know about facial treatments to achieve glowing, healthy skin.', 'Facial treatments are essential for maintaining healthy, radiant skin at any age. Our comprehensive guide covers everything from basic cleansing routines to advanced professional treatments. Whether you\'re dealing with acne, aging, or just want to maintain your skin\'s natural glow, the right facial treatment can make all the difference. We explore different types of facials including deep cleansing, hydrating, anti-aging, and specialized treatments for sensitive skin. Learn about the benefits of regular facials, how often you should get them, and what to expect during your treatment. Our licensed estheticians share their expert tips for at-home care between professional treatments, including product recommendations and techniques that will keep your skin looking its best. Remember, consistency is key when it comes to skincare, and professional treatments should be complemented with a good daily routine.', 'Facial Care', 'published', 'facial, skincare, treatments, beauty, skin health', True),
            ('Eyebrow Threading: Everything You Need to Know', 'eyebrow-threading-guide', 'Master the art of eyebrow threading with our comprehensive guide to perfect brows.', 'Eyebrow threading is one of the most precise and effective methods for shaping and maintaining beautiful eyebrows. This ancient technique uses a twisted cotton thread to remove unwanted hair, creating clean, defined lines that last longer than other hair removal methods. Our detailed guide covers the threading process, benefits, aftercare, and what to expect during your appointment. Threading is particularly effective for creating sharp, clean lines and is gentle on sensitive skin around the eyes. We discuss the difference between threading and other hair removal methods, how to prepare for your appointment, and tips for maintaining your brows between visits. Our experienced technicians share their secrets for achieving the perfect arch and shape that complements your face structure. Whether you prefer a natural look or a more dramatic arch, threading can help you achieve the brows of your dreams.', 'Threading', 'published', 'eyebrow, threading, beauty, grooming, brows', False),
            ('Hair Color Trends: From Natural to Bold', 'hair-color-trends-2024', 'Explore the hottest hair color trends that will make you stand out this year.', 'Hair color is one of the most powerful ways to express your personality and transform your entire look. In 2024, we\'re seeing an exciting mix of natural, sun-kissed tones and bold, statement-making colors. From the ever-popular balayage and highlights to vibrant fashion colors and rich, deep tones, there\'s something for everyone. Our color experts break down the latest trends, including the return of warm, golden tones, the popularity of dimensional coloring, and the rise of low-maintenance color techniques. We discuss how to choose the right color for your skin tone, hair type, and lifestyle. Whether you want a subtle change or a dramatic transformation, our professional colorists can help you achieve the perfect look. We also cover important topics like color maintenance, protecting your hair from damage, and how to transition between different color trends safely.', 'Hair Color', 'published', 'hair color, trends, balayage, highlights, beauty', False),
        ]

        for title, slug, excerpt, content, category, status, tags, is_featured in blog_posts_data:
            BlogPost.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'excerpt': excerpt,
                    'content': content,
                    'category': category,
                    'status': status,
                    'tags': tags,
                    'is_featured': is_featured,
                }
            )
        self.stdout.write('Created blog posts')

        # Create Theme Settings
        theme_settings, created = ThemeSettings.objects.get_or_create(
            name="Aarushi Salon Theme",
            defaults={
                'primary_color': '#8B5A3C',
                'secondary_color': '#A67C52',
                'accent_color': '#D4AF8C',
                'text_color': '#2c2c2c',
                'background_color': '#ffffff',
                'heading_font': 'Playfair Display',
                'body_font': 'Open Sans',
                'enable_gradients': True,
                'enable_animations': True,
                'enable_shadows': True,
                'is_active': True,
            }
        )
        self.stdout.write('Created theme settings')

        # Create Site Settings
        site_settings, created = SiteSettings.objects.get_or_create(
            site_name="Aarushi Salon",
            defaults={
                'site_tagline': 'Beauty & Wellness',
                'site_description': 'Professional beauty salon services including hair styling, makeup, skincare, massage, and more.',
                'phone': '+1 (555) 123-4567',
                'email': 'info@arushisalon.com',
                'address': 'Convenient salon located in a shopping district near Walmart',
                'facebook_url': 'https://facebook.com/arushisalon',
                'instagram_url': 'https://instagram.com/arushisalon',
                'linkedin_url': 'https://linkedin.com/company/arushisalon',
                'twitter_url': 'https://twitter.com/arushisalon',
                'is_active': True,
            }
        )
        self.stdout.write('Created site settings')

        # Create Service Icons
        service_icons_data = [
            ('Skin Care', 'fas fa-spa', '#8B5A3C', '#A67C52'),
            ('Hair Styling', 'fas fa-cut', '#8B5A3C', '#A67C52'),
            ('Color', 'fas fa-palette', '#8B5A3C', '#A67C52'),
            ('Waxing', 'fas fa-hand-holding-heart', '#8B5A3C', '#A67C52'),
            ('Threading', 'fas fa-hand-holding-heart', '#8B5A3C', '#A67C52'),
            ('Massage', 'fas fa-hands', '#8B5A3C', '#A67C52'),
            ('Make Up', 'fas fa-makeup', '#8B5A3C', '#A67C52'),
            ('Bridal Package', 'fas fa-makeup', '#8B5A3C', '#A67C52'),
            ('Herbal Bleach', 'fas fa-leaf', '#8B5A3C', '#A67C52'),
            ('Body Scrub', 'fas fa-leaf', '#8B5A3C', '#A67C52'),
            ('Henna Design', 'fas fa-paint-brush', '#8B5A3C', '#A67C52'),
        ]

        for category_name, icon_class, icon_color, bg_color in service_icons_data:
            try:
                category = ServiceCategory.objects.get(name=category_name)
                ServiceIcons.objects.get_or_create(
                    service_category=category,
                    defaults={
                        'icon_class': icon_class,
                        'icon_color': icon_color,
                        'background_color': bg_color,
                        'is_active': True,
                    }
                )
            except ServiceCategory.DoesNotExist:
                continue

        self.stdout.write('Created service icons')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with Aarushi Salon content!')
        )
