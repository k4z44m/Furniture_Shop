from django.urls import path
from .views import *

urlpatterns = [
    path('about/', about_us_view, name='about'),
    path('services/', services_view, name='services'),
    path('blog/', blog_view, name='blog'),
    path('contact/', contact_us_view, name='contact'),
    path('save_sub/', save_sub_view, name='save_sub'),
]
