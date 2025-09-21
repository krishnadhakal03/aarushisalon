from .models import ThemeSettings, SiteSettings, SiteImages, ServiceIcons

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

