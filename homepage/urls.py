from django.urls import path  # Import the path function for defining URL patterns
from . import views  # Import the views module from the current package

# Define the app name for namespacing in URL patterns
app_name = 'homepage'

# URL patterns for the homepage app
urlpatterns = [
    # Define url to map the 'homepage_view' function in views.py
    path('', views.homepage_view, name='homepage'),

    # Define a URL pattern for the blog_and_review view
    path('blogs&reviews/<int:pk>/', views.blog_and_review_detail_view, name='detail_blog_review'),

    # URL pattern for affiliate link generator page
    path('affiliate-link-generator/', views.affiliate_link_generator_view, name='affiliate_link_generator'),

    # URL pattern for shop page
    path('shop/', views.shop_view, name='shop'),

    # URL pattern for contact form submission
    path('contact/submit/', views.contact_form_submit, name='contact_form_submit'),
]
