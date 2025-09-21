from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost, Service, GalleryImage, TeamMember, Testimonial

class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'salon:home',
            'salon:about',
            'salon:services',
            'salon:gallery',
            'salon:team',
            'salon:testimonials',
            'salon:blog',
            'salon:contact',
            'salon:pricing',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        from django.utils import timezone
        return timezone.now()


class BlogPostSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(status='published', is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('salon:blog_detail', kwargs={'slug': obj.slug})


class ServiceSitemap(Sitemap):
    """Sitemap for services"""
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('salon:service_detail', kwargs={'pk': obj.pk})


class GallerySitemap(Sitemap):
    """Sitemap for gallery images"""
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return GalleryImage.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('salon:gallery')


class TeamSitemap(Sitemap):
    """Sitemap for team members"""
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return TeamMember.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('salon:team')


class TestimonialSitemap(Sitemap):
    """Sitemap for testimonials"""
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Testimonial.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('salon:testimonials')
