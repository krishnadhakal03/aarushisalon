from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
import json

from .models import (
    ServiceCategory, Service, TeamMember, Testimonial, 
    GalleryImage, BlogPost, ContactInfo, Appointment, SiteContent
)


def home(request):
    """Home page view"""
    # Get featured services
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:6]
    
    # Get all service categories for navigation
    service_categories = ServiceCategory.objects.filter(is_active=True)
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:4]
    
    # Get team members
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    
    # Get gallery images
    gallery_images = GalleryImage.objects.filter(is_active=True)[:6]
    
    # Get blog posts
    blog_posts = BlogPost.objects.filter(is_published=True)[:2]
    
    # Get site content
    site_content = {}
    for content in SiteContent.objects.filter(is_active=True):
        site_content[content.content_type] = content
    
    context = {
        'featured_services': featured_services,
        'service_categories': service_categories,
        'testimonials': testimonials,
        'team_members': team_members,
        'gallery_images': gallery_images,
        'blog_posts': blog_posts,
        'site_content': site_content,
    }
    
    return render(request, 'salon/home.html', context)


def about(request):
    """About page view"""
    team_members = TeamMember.objects.filter(is_active=True)
    site_content = {}
    for content in SiteContent.objects.filter(is_active=True):
        site_content[content.content_type] = content
    
    context = {
        'team_members': team_members,
        'site_content': site_content,
    }
    
    return render(request, 'salon/about.html', context)


def services(request):
    """Services page view"""
    service_categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
    
    context = {
        'service_categories': service_categories,
    }
    
    return render(request, 'salon/services.html', context)


def service_detail(request, service_id):
    """Individual service detail view"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    related_services = Service.objects.filter(
        category=service.category, 
        is_active=True
    ).exclude(id=service.id)[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    
    return render(request, 'salon/service_detail.html', context)


def pricing(request):
    """Pricing page view"""
    service_categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
    
    context = {
        'service_categories': service_categories,
    }
    
    return render(request, 'salon/pricing.html', context)


def gallery(request):
    """Gallery page view"""
    gallery_images = GalleryImage.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(gallery_images, 12)  # 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'gallery_images': page_obj,
    }
    
    return render(request, 'salon/gallery.html', context)


def team(request):
    """Team page view"""
    team_members = TeamMember.objects.filter(is_active=True)
    
    context = {
        'team_members': team_members,
    }
    
    return render(request, 'salon/team.html', context)


def testimonials(request):
    """Testimonials page view"""
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(testimonials, 6)  # 6 testimonials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'testimonials': page_obj,
    }
    
    return render(request, 'salon/testimonials.html', context)


def blog(request):
    """Blog page view"""
    blog_posts = BlogPost.objects.filter(is_published=True)
    
    # Pagination
    paginator = Paginator(blog_posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'blog_posts': page_obj,
    }
    
    return render(request, 'salon/blog.html', context)


def blog_detail(request, slug):
    """Individual blog post detail view"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'salon/blog_detail.html', context)


def contact(request):
    """Contact page view"""
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/contact.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def book_appointment(request):
    """Handle appointment booking via AJAX"""
    try:
        data = json.loads(request.body)
        
        # Create appointment
        appointment = Appointment.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            service_id=data.get('service_id'),
            preferred_date=data.get('preferred_date'),
            preferred_time=data.get('preferred_time'),
            message=data.get('message', ''),
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Appointment booked successfully! We will contact you soon.',
            'appointment_id': appointment.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error booking appointment: {str(e)}'
        }, status=400)