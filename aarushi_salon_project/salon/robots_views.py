from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

@cache_page(60 * 60 * 24)  # Cache for 24 hours
@require_http_methods(["GET"])
def robots_txt(request):
    """Generate robots.txt file"""
    context = {
        'domain': request.get_host(),
    }
    
    robots_content = render_to_string('robots.txt', context)
    return HttpResponse(robots_content, content_type='text/plain')
