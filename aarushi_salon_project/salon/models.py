from django.db import models
from django.utils import timezone


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For Font Awesome icons
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, blank=True)  # e.g., "60 minutes"
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100, blank=True)
    client_profession = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.profession}"


class CustomerFeedback(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=100, help_text="Your full name")
    email = models.EmailField(help_text="Your email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Your phone number (optional)")
    service_received = models.CharField(max_length=200, help_text="Service you received")
    rating = models.IntegerField(
        choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)],
        help_text="Rate your experience (1-5 stars)"
    )
    feedback = models.TextField(help_text="Share your experience with us")
    is_anonymous = models.BooleanField(default=False, help_text="Check to hide your name from public display")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Feedback"
        verbose_name_plural = "Customer Feedback"

    def __str__(self):
        display_name = "Anonymous" if self.is_anonymous else self.name
        return f"{display_name} - {self.rating} stars - {self.get_status_display()}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200, help_text="Blog post title")
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the title")
    content = models.TextField(help_text="Main blog content")
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short description for previews")
    image = models.ImageField(upload_to='blog/', blank=True, null=True, help_text="Main blog image")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, help_text="Featured image for homepage")
    author = models.CharField(max_length=100, default="Aarushi Salon")
    category = models.CharField(max_length=100, blank=True, help_text="Blog category (e.g., Hair Care, Skin Care)")
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags (e.g., hair, styling, tips)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', help_text="Publication status")
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    view_count = models.PositiveIntegerField(default=0, help_text="Number of views")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    @property
    def is_published(self):
        """Check if post is published"""
        return self.status == 'published'


class BlogComment(models.Model):
    """Blog post comments"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Comment"
        verbose_name_plural = "Blog Comments"
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"


class ContactInfo(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "Contact Information"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service.name}"


class SiteContent(models.Model):
    CONTENT_TYPES = [
        ('hero_title', 'Hero Title'),
        ('hero_subtitle', 'Hero Subtitle'),
        ('about_title', 'About Title'),
        ('about_subtitle', 'About Subtitle'),
        ('about_content', 'About Content'),
        ('experience_years', 'Experience Years'),
        ('happy_customers', 'Happy Customers'),
    ]

    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES, unique=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['content_type']

    def __str__(self):
        return f"{self.get_content_type_display()}"


class ThemeSettings(models.Model):
    """Theme customization settings"""
    name = models.CharField(max_length=100, default="Default Theme")
    is_active = models.BooleanField(default=True)
    
    # Logo and Branding
    logo = models.ImageField(upload_to='theme/', blank=True, null=True)
    favicon = models.ImageField(upload_to='theme/', blank=True, null=True)
    
    # Color Palette
    primary_color = models.CharField(max_length=7, default='#e91e63', help_text='Primary color (hex code)')
    secondary_color = models.CharField(max_length=7, default='#ff4081', help_text='Secondary color (hex code)')
    accent_color = models.CharField(max_length=7, default='#f50057', help_text='Accent color (hex code)')
    text_color = models.CharField(max_length=7, default='#2c2c2c', help_text='Text color (hex code)')
    background_color = models.CharField(max_length=7, default='#ffffff', help_text='Background color (hex code)')
    
    # Typography
    heading_font = models.CharField(max_length=100, default='Dancing Script', help_text='Font family for headings')
    body_font = models.CharField(max_length=100, default='Work Sans', help_text='Font family for body text')
    
    # Layout Settings
    enable_gradients = models.BooleanField(default=True)
    enable_animations = models.BooleanField(default=True)
    enable_shadows = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Theme Settings"
        verbose_name_plural = "Theme Settings"

    def __str__(self):
        return self.name


class SiteImages(models.Model):
    """Manage site images"""
    IMAGE_TYPES = [
        ('hero_bg', 'Hero Background'),
        ('about_bg', 'About Background'),
        ('gallery_bg', 'Gallery Background'),
        ('testimonial_bg', 'Testimonial Background'),
        ('contact_bg', 'Contact Background'),
        ('default_service', 'Default Service Image'),
        ('default_team', 'Default Team Image'),
        ('default_testimonial', 'Default Testimonial Image'),
    ]
    
    name = models.CharField(max_length=100)
    image_type = models.CharField(max_length=50, choices=IMAGE_TYPES)
    image = models.ImageField(upload_to='site_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Site Image"
        verbose_name_plural = "Site Images"

    def __str__(self):
        return f"{self.name} - {self.get_image_type_display()}"


class ServiceIcons(models.Model):
    """Manage service icons"""
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='icons')
    icon_class = models.CharField(max_length=100, help_text='Font Awesome icon class (e.g., fas fa-spa)')
    icon_color = models.CharField(max_length=7, default='#e91e63', help_text='Icon color (hex code)')
    background_color = models.CharField(max_length=7, default='#ff4081', help_text='Icon background color (hex code)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Icon"
        verbose_name_plural = "Service Icons"

    def __str__(self):
        return f"{self.service_category.name} - {self.icon_class}"


class SiteSettings(models.Model):
    """General site settings"""
    site_name = models.CharField(max_length=100, default="Aarushi Salon")
    site_tagline = models.CharField(max_length=200, default="Beauty & Wellness")
    site_description = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Contact Info
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Business Hours
    monday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    tuesday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    wednesday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    thursday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    friday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    saturday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    sunday_hours = models.CharField(max_length=50, default="10:00 AM - 6:00 PM")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name