from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .admin import admin_site, ServiceCategory, Service, TeamMember, Testimonial, GalleryImage, BlogPost, BlogComment, ContactInfo, Appointment, SiteContent, ThemeSettings, SiteImages, ServiceIcons, SiteSettings

# Register all models with our custom admin site
admin_site.register(ServiceCategory)
admin_site.register(Service)
admin_site.register(TeamMember)
admin_site.register(Testimonial)
admin_site.register(GalleryImage)
admin_site.register(BlogPost)
admin_site.register(BlogComment)
admin_site.register(ContactInfo)
admin_site.register(Appointment)
admin_site.register(SiteContent)
admin_site.register(ThemeSettings)
admin_site.register(SiteImages)
admin_site.register(ServiceIcons)
admin_site.register(SiteSettings)

# Custom admin URLs
admin_urlpatterns = [
    path('admin/', admin_site.urls),
    path('admin', lambda request: redirect('/admin/')),
]

