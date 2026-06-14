from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('cook/dashboard/', views.cook_dashboard, name='cook_dashboard'),
    path('cook/orders/', views.cook_orders, name='cook_orders'),
    path('cook/products/', views.cook_products, name='cook_products'),
    path('cook/request/', views.create_request, name='create_request'),
]