from .models import ThemeSettings, SiteSettings, SiteImages, ServiceIcons, SEOSettings, GoogleAnalytics

def theme_context(request):
    """Add theme settings to all templates"""
    try:
        theme = ThemeSettings.objects.filter(is_active=True).first()
        site_settings = SiteSettings.objects.filter(is_active=True).first()
    except:
        theme = None
        site_settings = None
    
    return {
        'theme_settings': theme,
        'site_settings': site_settings,
    }

def site_images_context(request):
    """Add site images to all templates"""
    try:
        images = {}
        for img in SiteImages.objects.filter(is_active=True):
            images[img.image_type] = img
    except:
        images = {}
    
    return {
        'site_images': images,
    }

def service_icons_context(request):
    """Add service icons to all templates"""
    try:
        icons = {}
        for icon in ServiceIcons.objects.filter(is_active=True):
            icons[icon.service_category.name] = icon
    except:
        icons = {}
    
    return {
        'service_icons': icons,
    }

def seo_context(request):
    """Add SEO settings to all templates"""
    try:
        # Get current page type from URL
        page_type = 'home'  # default
        path = request.path.strip('/')
        
        if path == '' or path == 'index.html':
            page_type = 'home'
        elif 'about' in path:
            page_type = 'about'
        elif 'services' in path:
            page_type = 'services'
        elif 'gallery' in path:
            page_type = 'gallery'
        elif 'team' in path:
            page_type = 'team'
        elif 'testimonials' in path:
            page_type = 'testimonials'
        elif 'blog' in path:
            page_type = 'blog'
        elif 'contact' in path:
            page_type = 'contact'
        elif 'pricing' in path:
            page_type = 'pricing'
        
        seo_settings = SEOSettings.objects.filter(page_type=page_type, is_active=True).first()
        analytics = GoogleAnalytics.objects.filter(is_active=True).first()
    except:
        seo_settings = None
        analytics = None
    
    return {
        'seo_settings': seo_settings,
        'analytics': analytics,
        'current_page_type': page_type,
    }

