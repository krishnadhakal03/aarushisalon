from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from django.template.loader import render_to_string
import json

from .models import (
    ServiceCategory, Service, TeamMember, Testimonial, 
    GalleryImage, BlogPost, ContactInfo, Appointment, SiteContent
)
from django.contrib import messages


def home(request):
    """Home page view"""
    # Get featured services
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:6]
    
    # Get all service categories for navigation
    service_categories = ServiceCategory.objects.filter(is_active=True)
    
    # Get testimonials (admin-created) - filter out empty content
    testimonials = Testimonial.objects.filter(
        is_active=True,
        content__isnull=False
    ).exclude(content__exact='')[:4]
    
    # Get customer feedback (using Testimonial model for now) - filter out empty content
    customer_feedback = Testimonial.objects.filter(
        is_active=True, 
        is_featured=True,
        content__isnull=False
    ).exclude(content__exact='')[:4]
    
    # Get team members
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    
    # Get gallery images
    gallery_images = GalleryImage.objects.filter(is_active=True)[:6]
    
    # Get blog posts
    blog_posts = BlogPost.objects.filter(status='published')[:2]
    
    # Get site content
    site_content = {}
    for content in SiteContent.objects.filter(is_active=True):
        site_content[content.content_type] = content
    
    # Get contact info
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    # Handle feedback form submission
    if request.method == 'POST' and 'feedback_submit' in request.POST:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        service_received = request.POST.get('service_received', '').strip()
        rating = request.POST.get('rating', '5')
        feedback_text = request.POST.get('feedback', '').strip()
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        # Validate required fields
        if not name or not email or not service_received or not feedback_text:
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                # Create new testimonial
                testimonial = Testimonial.objects.create(
                    client_name='Anonymous' if is_anonymous else name,
                    client_profession=service_received,
                    content=feedback_text,
                    rating=int(rating),
                    is_active=True,  # Set to active to show immediately
                    is_featured=True  # Set as featured to show in slider
                )
                messages.success(request, 'Thank you for your feedback! Your review has been added.')
                return redirect('salon:home')
            except Exception as e:
                messages.error(request, 'There was an error submitting your feedback. Please try again.')
    
    # Create form data for template
    feedback_form_data = {
        'name': request.POST.get('name', '') if request.method == 'POST' else '',
        'email': request.POST.get('email', '') if request.method == 'POST' else '',
        'service_received': request.POST.get('service_received', '') if request.method == 'POST' else '',
        'rating': request.POST.get('rating', '5') if request.method == 'POST' else '5',
        'feedback': request.POST.get('feedback', '') if request.method == 'POST' else '',
        'is_anonymous': request.POST.get('is_anonymous') == 'on' if request.method == 'POST' else False,
    }
    
    context = {
        'featured_services': featured_services,
        'service_categories': service_categories,
        'testimonials': testimonials,
        'customer_feedback': customer_feedback,
        'feedback_form_data': feedback_form_data,
        'team_members': team_members,
        'gallery_images': gallery_images,
        'blog_posts': blog_posts,
        'site_content': site_content,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/home_perfectcut.html', context)


def about(request):
    """About page view"""
    team_members = TeamMember.objects.filter(is_active=True)
    site_content = {}
    for content in SiteContent.objects.filter(is_active=True):
        site_content[content.content_type] = content
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'team_members': team_members,
        'site_content': site_content,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/about_perfectcut.html', context)


def services(request):
    """Services page view"""
    service_categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'service_categories': service_categories,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/services_perfectcut.html', context)


def service_detail(request, service_id):
    """Individual service detail view"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    related_services = Service.objects.filter(
        category=service.category, 
        is_active=True
    ).exclude(id=service.id)[:3]
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'service': service,
        'related_services': related_services,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/service_detail_perfectcut.html', context)


def pricing(request):
    """Pricing page view"""
    service_categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'service_categories': service_categories,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/pricing_perfectcut.html', context)


def gallery(request):
    """Gallery page view"""
    # Get category filter from URL
    category_filter = request.GET.get('category', 'all')
    
    # Filter out images that don't have actual files
    gallery_images = []
    for img in GalleryImage.objects.filter(is_active=True):
        try:
            # Check if the image file exists
            if img.image and img.image.name:
                # Try to access the image to see if it exists
                img.image.url
                
                # Apply category filter
                if category_filter == 'all':
                    gallery_images.append(img)
                else:
                    # Map URL categories to actual categories
                    category_mapping = {
                        'skin-care': 'Skin Care',
                        'hair-styling': 'Hair Styling',
                        'make-up': 'Make Up',
                        'waxing': 'Waxing',
                        'massage': 'Massage',
                        'threading': 'Threading',
                        'color': 'Color',
                        'bridal-package': 'Bridal Package',
                        'manicure': 'Manicure',
                        'pedicure': 'Pedicure',
                    }
                    
                    target_category = category_mapping.get(category_filter)
                    if target_category and target_category in img.title:
                        gallery_images.append(img)
                        
        except (ValueError, FileNotFoundError):
            # Skip images without files
            continue
    
    # Pagination
    paginator = Paginator(gallery_images, 12)  # 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'page_obj': page_obj,
        'gallery_images': page_obj,
        'contact_info': contact_info,
        'current_category': category_filter,
    }
    
    return render(request, 'salon/gallery_perfectcut.html', context)


def team(request):
    """Team page view"""
    team_members = TeamMember.objects.filter(is_active=True)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'team_members': team_members,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/team_perfectcut.html', context)


def testimonials(request):
    """Testimonials page view"""
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(testimonials, 6)  # 6 testimonials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'page_obj': page_obj,
        'testimonials': page_obj,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/testimonials_perfectcut.html', context)


def blog(request):
    """Blog page view"""
    blog_posts = BlogPost.objects.filter(status='published')
    
    # Pagination
    paginator = Paginator(blog_posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'page_obj': page_obj,
        'blog_posts': page_obj,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/blog_perfectcut.html', context)


def blog_detail(request, slug):
    """Individual blog post detail view"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    post.view_count += 1
    post.save(update_fields=['view_count'])
    
    # Handle comment submission
    if request.method == 'POST':
        from .models import BlogComment
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')
        
        if name and email and comment_text:
            BlogComment.objects.create(
                post=post,
                name=name,
                email=email,
                comment=comment_text
            )
            messages.success(request, 'Your comment has been submitted and will be reviewed.')
            return redirect('salon:blog_detail', slug=slug)
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True)
    
    recent_posts = BlogPost.objects.filter(
        status='published'
    ).exclude(id=post.id)[:3]
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'post': post,
        'comments': comments,
        'recent_posts': recent_posts,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/blog_detail_perfectcut.html', context)


def contact(request):
    """Contact page view"""
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/contact_perfectcut.html', context)


def book_appointment(request):
    """Appointment booking page"""
    if request.method == 'POST':
        try:
            # Create appointment
            appointment = Appointment.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                service_id=request.POST.get('service_id'),
                preferred_date=request.POST.get('preferred_date'),
                preferred_time=request.POST.get('preferred_time'),
                message=request.POST.get('message', ''),
            )
            
            messages.success(request, 'Appointment booked successfully! We will contact you soon.')
            return redirect('salon:book_appointment')
            
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
    
    # Get services for the form
    services = Service.objects.filter(is_active=True)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'services': services,
        'contact_info': contact_info,
    }
    
    return render(request, 'salon/book_appointment_perfectcut.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def book_appointment_ajax(request):
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


def dynamic_theme_css(request):
    """Serve dynamic CSS based on theme settings"""
    css_content = render_to_string('salon/dynamic_theme.css')
    response = HttpResponse(css_content, content_type='text/css')
    response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    return response