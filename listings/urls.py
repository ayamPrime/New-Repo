from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('listings/', views.listings_page, name = 'listings'),
    path('create_listings/', views.add_listings, name = 'create_listings'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
]