from django.urls import path
from django.shortcuts import redirect
from .admin import admin_site

# Custom admin URLs
admin_urlpatterns = [
    path('admin/', admin_site.urls),
    path('admin', lambda request: redirect('/admin/')),
]


