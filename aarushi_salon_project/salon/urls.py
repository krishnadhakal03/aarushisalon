from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import StaticViewSitemap, BlogPostSitemap, ServiceSitemap, GallerySitemap, TeamSitemap, TestimonialSitemap
from .robots_views import robots_txt
from .api_views import GetAvailableSlotsView, GetAvailableDatesView, CheckSlotAvailabilityView, get_services_api

app_name = 'salon'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('pricing/', views.pricing, name='pricing'),
    path('gallery/', views.gallery, name='gallery'),
    path('team/', views.team, name='team'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact_simple, name='contact'),
    path('book-appointment/', views.book_appointment_simple, name='book_appointment'),
    path('dynamic-theme.css', views.dynamic_theme_css, name='dynamic_theme_css'),
    
    # API URLs for appointment booking
    path('api/available-slots/', GetAvailableSlotsView.as_view(), name='available_slots_api'),
    path('api/available-dates/', GetAvailableDatesView.as_view(), name='available_dates_api'),
    path('api/check-slot-availability/', CheckSlotAvailabilityView.as_view(), name='check_slot_availability_api'),
    path('api/services/', get_services_api, name='services_api'),
    
    # SEO URLs
    path('sitemap.xml', sitemap, {
        'sitemaps': {
            'static': StaticViewSitemap,
            'blog': BlogPostSitemap,
            'services': ServiceSitemap,
            'gallery': GallerySitemap,
            'team': TeamSitemap,
            'testimonials': TestimonialSitemap,
        }
    }, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]
