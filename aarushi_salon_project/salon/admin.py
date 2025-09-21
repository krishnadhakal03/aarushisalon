from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils import timezone
from .models import (
    ServiceCategory, Service, TeamMember, Testimonial, 
    GalleryImage, BlogPost, BlogComment, ContactInfo, Appointment, SiteContent,
    ThemeSettings, SiteImages, ServiceIcons, SiteSettings, CustomerFeedback
)

# Custom Admin Site
class AarushiSalonAdminSite(admin.AdminSite):
    site_header = "Aarushi Salon Administration"
    site_title = "Aarushi Salon Admin"
    index_title = "Welcome to Aarushi Salon Admin"
    site_url = "/"

admin_site = AarushiSalonAdminSite(name='aarushi_admin')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description'),
            'description': 'Enter the category name and a brief description. This will be displayed on your website.'
        }),
        ('Settings', {
            'fields': ('is_active',),
            'description': 'Check "Is active" to show this category on your website.'
        }),
    )
    
    def service_count(self, obj):
        count = obj.services.count()
        if count > 0:
            url = reverse('admin:salon_service_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} services</a>', url, count)
        return '0 services'
    service_count.short_description = 'Services'
    service_count.admin_order_field = 'services__count'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_display', 'duration_display', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    list_editable = ['is_featured', 'is_active']
    ordering = ['category__name', 'name']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'category', 'description'),
            'description': 'Enter the service name, select a category, and provide a detailed description.'
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration'),
            'description': 'Set the price and duration for this service. Duration is optional.'
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active'),
            'description': 'Featured services appear prominently on your website. Active services are visible to customers.'
        }),
    )
    
    def price_display(self, obj):
        return f"${obj.price}"
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'
    
    def duration_display(self, obj):
        if obj.duration:
            return f"{obj.duration} min"
        return "Not set"
    duration_display.short_description = 'Duration'
    duration_display.admin_order_field = 'duration'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'specialization', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position', 'bio', 'specialization']
    list_editable = ['is_active']
    ordering = ['name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'position', 'specialization'),
            'description': 'Enter the team member\'s name, position, and area of specialization.'
        }),
        ('Bio & Image', {
            'fields': ('bio', 'image'),
            'description': 'Add a professional bio and upload a high-quality photo of the team member.'
        }),
        ('Settings', {
            'fields': ('is_active',),
            'description': 'Check "Is active" to display this team member on your website.'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'profession', 'rating', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['client_name', 'profession', 'content']
    list_editable = ['is_featured', 'is_active']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'view_count', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'author', 'category', 'tags']
    list_editable = ['status', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'status', 'is_featured'),
            'description': 'Enter the blog post title, author, and category. The slug will be auto-generated from the title.'
        }),
        ('Content', {
            'fields': ('excerpt', 'content'),
            'classes': ('wide',)
        }),
        ('Images', {
            'fields': ('image', 'featured_image'),
            'classes': ('collapse',)
        }),
        ('SEO & Tags', {
            'fields': ('tags', 'view_count'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post']
    search_fields = ['name', 'email', 'comment', 'post__title']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'service', 'preferred_date', 'preferred_time', 'status', 'created_at']
    list_filter = ['status', 'preferred_date', 'service__category', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'service__name']
    list_editable = ['status']
    date_hierarchy = 'preferred_date'


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'title', 'is_active', 'updated_at']
    list_filter = ['content_type', 'is_active', 'updated_at']
    search_fields = ['title', 'content']


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'primary_color', 'secondary_color', 'created_at']
    list_filter = ['is_active', 'enable_gradients', 'enable_animations']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'is_active')
        }),
        ('Logo & Branding', {
            'fields': ('logo', 'favicon')
        }),
        ('Color Palette', {
            'fields': ('primary_color', 'secondary_color', 'accent_color', 'text_color', 'background_color'),
            'classes': ('wide',)
        }),
        ('Typography', {
            'fields': ('heading_font', 'body_font')
        }),
        ('Layout Options', {
            'fields': ('enable_gradients', 'enable_animations', 'enable_shadows'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteImages)
class SiteImagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_type', 'is_active', 'created_at']
    list_filter = ['image_type', 'is_active']
    search_fields = ['name', 'alt_text']


@admin.register(ServiceIcons)
class ServiceIconsAdmin(admin.ModelAdmin):
    list_display = ['service_category', 'icon_class', 'icon_color', 'is_active']
    list_filter = ['is_active', 'service_category']
    search_fields = ['service_category__name', 'icon_class']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'is_active']
    fieldsets = (
        ('Basic Info', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('Business Hours', {
            'fields': ('monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours', 
                      'friday_hours', 'saturday_hours', 'sunday_hours'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service_received', 'rating', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'rating', 'is_featured', 'is_anonymous', 'created_at']
    search_fields = ['name', 'email', 'service_received', 'feedback']
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone', 'is_anonymous'),
            'description': 'Customer contact information and privacy preferences.'
        }),
        ('Service & Experience', {
            'fields': ('service_received', 'rating', 'feedback'),
            'description': 'Details about the service received and customer experience.'
        }),
        ('Moderation', {
            'fields': ('status', 'is_featured'),
            'description': 'Review and approve feedback for public display.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'description': 'When the feedback was submitted and last updated.',
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()