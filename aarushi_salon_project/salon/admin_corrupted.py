from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils import timezone
from .models import (
    ServiceCategory, Service, TeamMember, Testimonial, 
    GalleryImage, BlogPost, BlogComment, ContactInfo, Appointment, SiteContent,
    ThemeSettings, SiteImages, ServiceIcons, SiteSettings, CustomerFeedback, ColorPalette
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
    list_display = ['name', 'description_preview', 'service_count', 'is_active', 'created_at', 'actions_column']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']
    list_per_page = 25
    
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
    
    def description_preview(self, obj):
        """Show truncated description"""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    description_preview.short_description = 'Description'
    
    def service_count(self, obj):
        count = obj.services.count()
        if count > 0:
            url = reverse('admin:salon_service_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} services</a>', url, count)
        return '0 services'
    service_count.short_description = 'Services'
    service_count.admin_order_field = 'services__count'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_servicecategory_change', args=[obj.id])
        delete_url = reverse('admin:salon_servicecategory_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description_preview', 'price_display', 'duration_display', 'is_featured', 'is_active', 'created_at', 'actions_column']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    list_editable = ['is_featured', 'is_active']
    ordering = ['category__name', 'name']
    list_per_page = 25
    
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
    
    def description_preview(self, obj):
        """Show truncated description"""
        if obj.description:
            return obj.description[:60] + '...' if len(obj.description) > 60 else obj.description
        return '-'
    description_preview.short_description = 'Description'
    
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
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_service_change', args=[obj.id])
        delete_url = reverse('admin:salon_service_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'specialization', 'bio_preview', 'social_links', 'is_active', 'created_at', 'actions_column']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position', 'bio', 'specialization']
    list_editable = ['is_active']
    ordering = ['name']
    list_per_page = 25
    
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
    
    def bio_preview(self, obj):
        """Show truncated bio"""
        if obj.bio:
            return obj.bio[:50] + '...' if len(obj.bio) > 50 else obj.bio
        return '-'
    bio_preview.short_description = 'Bio'
    
    def social_links(self, obj):
        """Show social media links count"""
        links = []
        if obj.facebook_url:
            links.append('FB')
        if obj.instagram_url:
            links.append('IG')
        if obj.linkedin_url:
            links.append('LI')
        return ', '.join(links) if links else 'None'
    social_links.short_description = 'Social Links'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_teammember_change', args=[obj.id])
        delete_url = reverse('admin:salon_teammember_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'profession', 'content_preview', 'rating_stars', 'is_featured', 'is_active', 'created_at', 'actions_column']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['client_name', 'profession', 'content']
    list_editable = ['is_featured', 'is_active']
    list_per_page = 25
    
    def content_preview(self, obj):
        """Show truncated content"""
        if obj.content:
            return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
        return '-'
    content_preview.short_description = 'Content'
    
    def rating_stars(self, obj):
        """Show rating as stars"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)
    rating_stars.short_description = 'Rating'
    rating_stars.admin_order_field = 'rating'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_testimonial_change', args=[obj.id])
        delete_url = reverse('admin:salon_testimonial_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'description_preview', 'image_thumbnail', 'category', 'is_featured', 'is_active', 'created_at', 'actions_column']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'category']
    list_editable = ['is_featured', 'is_active']
    list_per_page = 25
    
    def description_preview(self, obj):
        """Show truncated description"""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    description_preview.short_description = 'Description'
    
    def image_thumbnail(self, obj):
        """Show image thumbnail"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;">', obj.image.url)
        return 'No Image'
    image_thumbnail.short_description = 'Image'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_galleryimage_change', args=[obj.id])
        delete_url = reverse('admin:salon_galleryimage_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_preview', 'author', 'category', 'status', 'is_featured', 'view_count', 'created_at', 'actions_column']
    list_filter = ['status', 'is_featured', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'author', 'category', 'tags']
    list_editable = ['status', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    list_per_page = 25
    
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
    
    def content_preview(self, obj):
        """Show truncated content"""
        if obj.content:
            return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
        return '-'
    content_preview.short_description = 'Content'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_blogpost_change', args=[obj.id])
        delete_url = reverse('admin:salon_blogpost_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment_preview', 'post', 'is_approved', 'created_at', 'actions_column']
    list_filter = ['is_approved', 'created_at', 'post']
    search_fields = ['name', 'email', 'comment', 'post__title']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']
    list_per_page = 25
    
    def comment_preview(self, obj):
        """Show truncated comment"""
        if obj.comment:
            return obj.comment[:60] + '...' if len(obj.comment) > 60 else obj.comment
        return '-'
    comment_preview.short_description = 'Comment'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_blogcomment_change', args=[obj.id])
        delete_url = reverse('admin:salon_blogcomment_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'address_preview', 'is_active', 'updated_at', 'actions_column']
    list_filter = ['is_active', 'updated_at']
    list_per_page = 25
    
    def address_preview(self, obj):
        """Show truncated address"""
        if obj.address:
            return obj.address[:50] + '...' if len(obj.address) > 50 else obj.address
        return '-'
    address_preview.short_description = 'Address'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_contactinfo_change', args=[obj.id])
        delete_url = reverse('admin:salon_contactinfo_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'service', 'appointment_datetime', 'status', 'phone', 'email', 'created_at', 'actions_column']
    list_filter = ['status', 'preferred_date', 'service__category', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'service__name']
    list_editable = ['status']
    date_hierarchy = 'preferred_date'
    list_per_page = 25
    
    def client_name(self, obj):
        """Show full client name"""
        return f"{obj.first_name} {obj.last_name}"
    client_name.short_description = 'Client Name'
    client_name.admin_order_field = 'first_name'
    
    def appointment_datetime(self, obj):
        """Show formatted appointment date and time"""
        return f"{obj.preferred_date} at {obj.preferred_time}"
    appointment_datetime.short_description = 'Appointment'
    appointment_datetime.admin_order_field = 'preferred_date'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_appointment_change', args=[obj.id])
        delete_url = reverse('admin:salon_appointment_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'title', 'content_preview', 'is_active', 'updated_at', 'actions_column']
    list_filter = ['content_type', 'is_active', 'updated_at']
    search_fields = ['title', 'content']
    list_per_page = 25
    
    def content_preview(self, obj):
        """Show truncated content"""
        if obj.content:
            return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
        return '-'
    content_preview.short_description = 'Content'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_sitecontent_change', args=[obj.id])
        delete_url = reverse('admin:salon_sitecontent_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'color_palette', 'created_at', 'actions_column']
    list_filter = ['is_active', 'enable_gradients', 'enable_animations', 'color_palette']
    search_fields = ['name']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'is_active')
        }),
        ('Logo & Branding', {
            'fields': ('logo', 'favicon')
        }),
        ('Color Palette Selection', {
            'fields': ('color_palette',),
            'description': 'Select a predefined color palette for your theme.'
        }),
        ('Custom Color Overrides', {
            'fields': ('custom_primary_color', 'custom_secondary_color', 'custom_accent_color'),
            'description': 'Override specific colors from the selected palette (optional).',
            'classes': ('collapse',)
        }),
        ('Typography', {
            'fields': ('heading_font', 'body_font')
        }),
        ('Layout Options', {
            'fields': ('enable_gradients', 'enable_animations', 'enable_shadows'),
            'classes': ('collapse',)
        }),
    )
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_themesettings_change', args=[obj.id])
        delete_url = reverse('admin:salon_themesettings_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('color_palette')


@admin.register(SiteImages)
class SiteImagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_type', 'image_thumbnail', 'alt_text_preview', 'is_active', 'created_at', 'actions_column']
    list_filter = ['image_type', 'is_active', 'created_at']
    search_fields = ['name', 'alt_text']
    list_per_page = 25
    
    def image_thumbnail(self, obj):
        """Show image thumbnail"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;">', obj.image.url)
        return 'No Image'
    image_thumbnail.short_description = 'Image'
    
    def alt_text_preview(self, obj):
        """Show truncated alt text"""
        if obj.alt_text:
            return obj.alt_text[:30] + '...' if len(obj.alt_text) > 30 else obj.alt_text
        return '-'
    alt_text_preview.short_description = 'Alt Text'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_siteimages_change', args=[obj.id])
        delete_url = reverse('admin:salon_siteimages_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(ServiceIcons)
class ServiceIconsAdmin(admin.ModelAdmin):
    list_display = ['service_category', 'icon_class', 'icon_color', 'is_active', 'actions_column']
    list_filter = ['is_active', 'service_category']
    search_fields = ['service_category__name', 'icon_class']
    list_per_page = 25
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_serviceicons_change', args=[obj.id])
        delete_url = reverse('admin:salon_serviceicons_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'address_preview', 'is_active', 'actions_column']
    list_filter = ['is_active']
    search_fields = ['site_name', 'phone', 'email', 'address']
    list_per_page = 25
    
    def address_preview(self, obj):
        """Show truncated address"""
        if obj.address:
            return obj.address[:50] + '...' if len(obj.address) > 50 else obj.address
        return '-'
    address_preview.short_description = 'Address'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_sitesettings_change', args=[obj.id])
        delete_url = reverse('admin:salon_sitesettings_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True
    
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
    list_display = ['name', 'email', 'service_received', 'rating_stars', 'feedback_preview', 'status', 'is_featured', 'created_at', 'actions_column']
    list_filter = ['status', 'rating', 'is_featured', 'is_anonymous', 'created_at']
    search_fields = ['name', 'email', 'service_received', 'feedback']
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
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
    
    def rating_stars(self, obj):
        """Show rating as stars"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)
    rating_stars.short_description = 'Rating'
    rating_stars.admin_order_field = 'rating'
    
    def feedback_preview(self, obj):
        """Show truncated feedback"""
        if obj.feedback:
            return obj.feedback[:60] + '...' if len(obj.feedback) > 60 else obj.feedback
        return '-'
    feedback_preview.short_description = 'Feedback'
    
    def actions_column(self, obj):
        """Add edit and delete buttons"""
        edit_url = reverse('admin:salon_customerfeedback_change', args=[obj.id])
        delete_url = reverse('admin:salon_customerfeedback_delete', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            edit_url, delete_url
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()@ a d m i n . r e g i s t e r ( C o l o r P a l e t t e ) 
 
 c l a s s   C o l o r P a l e t t e A d m i n ( a d m i n . M o d e l A d m i n ) : 
 
         l i s t _ d i s p l a y   =   [ ' n a m e ' ,   ' d i s p l a y _ n a m e ' ,   ' c o l o r _ p r e v i e w ' ,   ' i s _ a c t i v e ' ,   ' c r e a t e d _ a t ' ,   ' a c t i o n s _ c o l u m n ' ] 
 
         l i s t _ f i l t e r   =   [ ' i s _ a c t i v e ' ,   ' c r e a t e d _ a t ' ] 
 
         s e a r c h _ f i e l d s   =   [ ' n a m e ' ,   ' d i s p l a y _ n a m e ' ] 
 
         l i s t _ e d i t a b l e   =   [ ' i s _ a c t i v e ' ] 
 
         l i s t _ p e r _ p a g e   =   2 5 
 
         
 
         f i e l d s e t s   =   ( 
 
                 ( ' B a s i c   I n f o r m a t i o n ' ,   { 
 
                         ' f i e l d s ' :   ( ' n a m e ' ,   ' d i s p l a y _ n a m e ' ,   ' i s _ a c t i v e ' ) , 
 
                         ' d e s c r i p t i o n ' :   ' E n t e r   t h e   p a l e t t e   n a m e   a n d   d i s p l a y   n a m e   f o r   t h e   a d m i n   i n t e r f a c e . ' 
 
                 } ) , 
 
                 ( ' P r i m a r y   C o l o r s ' ,   { 
 
                         ' f i e l d s ' :   ( ' p r i m a r y _ c o l o r ' ,   ' s e c o n d a r y _ c o l o r ' ,   ' a c c e n t _ c o l o r ' ) , 
 
                         ' d e s c r i p t i o n ' :   ' M a i n   b r a n d   c o l o r s   u s e d   t h r o u g h o u t   t h e   s i t e . ' 
 
                 } ) , 
 
                 ( ' T e x t   &   B a c k g r o u n d ' ,   { 
 
                         ' f i e l d s ' :   ( ' t e x t _ c o l o r ' ,   ' b a c k g r o u n d _ c o l o r ' ,   ' b o r d e r _ c o l o r ' ) , 
 
                         ' d e s c r i p t i o n ' :   ' C o l o r s   f o r   t e x t ,   b a c k g r o u n d s ,   a n d   b o r d e r s . ' 
 
                 } ) , 
 
                 ( ' S t a t u s   C o l o r s ' ,   { 
 
                         ' f i e l d s ' :   ( ' s u c c e s s _ c o l o r ' ,   ' w a r n i n g _ c o l o r ' ,   ' e r r o r _ c o l o r ' ,   ' i n f o _ c o l o r ' ) , 
 
                         ' d e s c r i p t i o n ' :   ' C o l o r s   f o r   s t a t u s   m e s s a g e s   a n d   a l e r t s . ' , 
 
                         ' c l a s s e s ' :   ( ' c o l l a p s e ' , ) 
 
                 } ) , 
 
         ) 
 
         
 
         d e f   c o l o r _ p r e v i e w ( s e l f ,   o b j ) : 
 
                 " " " S h o w   c o l o r   p r e v i e w " " " 
 
                 r e t u r n   f o r m a t _ h t m l ( 
 
                         ' < d i v   s t y l e = " d i s p l a y :   f l e x ;   g a p :   5 p x ;   a l i g n - i t e m s :   c e n t e r ; " > ' 
 
                         ' < d i v   s t y l e = " w i d t h :   2 0 p x ;   h e i g h t :   2 0 p x ;   b a c k g r o u n d - c o l o r :   { } ;   b o r d e r :   1 p x   s o l i d   # c c c ;   b o r d e r - r a d i u s :   3 p x ; " > < / d i v > ' 
 
                         ' < d i v   s t y l e = " w i d t h :   2 0 p x ;   h e i g h t :   2 0 p x ;   b a c k g r o u n d - c o l o r :   { } ;   b o r d e r :   1 p x   s o l i d   # c c c ;   b o r d e r - r a d i u s :   3 p x ; " > < / d i v > ' 
 
                         ' < d i v   s t y l e = " w i d t h :   2 0 p x ;   h e i g h t :   2 0 p x ;   b a c k g r o u n d - c o l o r :   { } ;   b o r d e r :   1 p x   s o l i d   # c c c ;   b o r d e r - r a d i u s :   3 p x ; " > < / d i v > ' 
 
                         ' < / d i v > ' , 
 
                         o b j . p r i m a r y _ c o l o r ,   o b j . s e c o n d a r y _ c o l o r ,   o b j . a c c e n t _ c o l o r 
 
                 ) 
 
         c o l o r _ p r e v i e w . s h o r t _ d e s c r i p t i o n   =   ' C o l o r   P r e v i e w ' 
 
         
 
         d e f   a c t i o n s _ c o l u m n ( s e l f ,   o b j ) : 
 
                 " " " A d d   e d i t   a n d   d e l e t e   b u t t o n s " " " 
 
                 e d i t _ u r l   =   r e v e r s e ( ' a d m i n : s a l o n _ c o l o r p a l e t t e _ c h a n g e ' ,   a r g s = [ o b j . i d ] ) 
 
                 d e l e t e _ u r l   =   r e v e r s e ( ' a d m i n : s a l o n _ c o l o r p a l e t t e _ d e l e t e ' ,   a r g s = [ o b j . i d ] ) 
 
                 r e t u r n   f o r m a t _ h t m l ( 
 
                         ' < a   h r e f = " { } "   c l a s s = " b t n   b t n - s m   b t n - p r i m a r y   m e - 1 " > E d i t < / a > ' 
 
                         ' < a   h r e f = " { } "   c l a s s = " b t n   b t n - s m   b t n - d a n g e r "   o n c l i c k = " r e t u r n   c o n f i r m ( \ ' A r e   y o u   s u r e ? \ ' ) " > D e l e t e < / a > ' , 
 
                         e d i t _ u r l ,   d e l e t e _ u r l 
 
                 ) 
 
         a c t i o n s _ c o l u m n . s h o r t _ d e s c r i p t i o n   =   ' A c t i o n s ' 
 
         a c t i o n s _ c o l u m n . a l l o w _ t a g s   =   T r u e 
 
 