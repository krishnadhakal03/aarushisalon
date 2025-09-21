from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import (
    ServiceCategory, Service, TeamMember, Testimonial, CustomerFeedback,
    GalleryImage, BlogPost, BlogComment, ContactInfo, Appointment,
    SiteContent, ThemeSettings, SiteImages, ServiceIcons, SiteSettings
)


class CustomAdminSite(AdminSite):
    site_header = "Aarushi Salon Administration"
    site_title = "Aarushi Salon Admin"
    index_title = "Welcome to Aarushi Salon Administration"
    site_url = "/"


# Create custom admin site instance
admin_site = CustomAdminSite(name='custom_admin')


@admin.register(ServiceCategory, site=admin_site)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']


@admin.register(Service, site=admin_site)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    list_editable = ['is_featured', 'is_active']
    ordering = ['category', 'name']
    raw_id_fields = ['category']


@admin.register(TeamMember, site=admin_site)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'specialization', 'is_active', 'created_at']
    list_filter = ['is_active', 'position', 'created_at']
    search_fields = ['name', 'position', 'specialization', 'bio']
    list_editable = ['is_active']
    ordering = ['name']


@admin.register(Testimonial, site=admin_site)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'profession', 'rating', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['client_name', 'profession', 'content']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-created_at']


@admin.register(CustomerFeedback, site=admin_site)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_received', 'rating', 'status', 'is_featured', 'created_at']
    list_filter = ['rating', 'status', 'is_featured', 'is_anonymous', 'created_at']
    search_fields = ['name', 'email', 'service_received', 'feedback']
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GalleryImage, site=admin_site)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-created_at']


@admin.register(BlogPost, site=admin_site)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'view_count', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'author', 'category', 'tags']
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogComment, site=admin_site)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'comment', 'post__title']
    list_editable = ['is_approved']
    ordering = ['-created_at']
    raw_id_fields = ['post']


@admin.register(ContactInfo, site=admin_site)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['phone', 'email', 'address']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Appointment, site=admin_site)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'service', 'preferred_date', 'preferred_time', 'status', 'created_at']
    list_filter = ['status', 'preferred_date', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'service__name']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['service']


@admin.register(SiteContent, site=admin_site)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'title', 'is_active', 'updated_at']
    list_filter = ['content_type', 'is_active', 'created_at', 'updated_at']
    search_fields = ['content_type', 'title', 'content']
    list_editable = ['is_active']
    ordering = ['content_type']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ThemeSettings, site=admin_site)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'primary_color', 'secondary_color', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Settings', {
            'fields': ('name', 'is_active')
        }),
        ('Logo & Branding', {
            'fields': ('logo', 'favicon')
        }),
        ('Color Palette', {
            'fields': ('primary_color', 'secondary_color', 'accent_color', 'text_color', 'background_color')
        }),
        ('Typography', {
            'fields': ('heading_font', 'body_font')
        }),
        ('Layout Settings', {
            'fields': ('enable_gradients', 'enable_animations', 'enable_shadows')
        }),
    )


@admin.register(SiteImages, site=admin_site)
class SiteImagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_type', 'is_active', 'created_at']
    list_filter = ['image_type', 'is_active', 'created_at']
    search_fields = ['name', 'alt_text']
    list_editable = ['is_active']
    ordering = ['image_type', 'name']


@admin.register(ServiceIcons, site=admin_site)
class ServiceIconsAdmin(admin.ModelAdmin):
    list_display = ['service_category', 'icon_class', 'icon_color', 'is_active', 'created_at']
    list_filter = ['is_active', 'service_category', 'created_at']
    search_fields = ['service_category__name', 'icon_class']
    list_editable = ['is_active']
    ordering = ['service_category', 'icon_class']
    raw_id_fields = ['service_category']


@admin.register(SiteSettings, site=admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_tagline', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['site_name', 'site_tagline', 'site_description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url')
        }),
        ('Business Hours', {
            'fields': ('monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours', 
                      'friday_hours', 'saturday_hours', 'sunday_hours')
        }),
    )


# Custom admin URLs
admin_urlpatterns = [
    path('admin/', admin_site.urls),
    path('admin', lambda request: redirect('/admin/')),
]
